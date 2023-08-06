import functools

import sklearn.cross_decomposition
from cython.parallel import prange
import pandas as pd
import numpy as np
cimport numpy as np
import scipy.stats

import wrenlab.util

def standardize(np.ndarray[np.float64_t, ndim=1] x):
    ix = ~np.isnan(x)
    mu, std = x[ix].mean(), x[ix].std()
    return (x - mu) / std

cdef _pearson(np.ndarray[np.float64_t, ndim=2] X, np.ndarray[np.float64_t, ndim=1] y):
    assert X.shape[1] == y.shape[0]
    ix = ~np.isnan(y)
    assert ix.sum() >= 3
    ns = X.shape[0]
    no = ix.sum()
    X = X[:,ix]

    Xs = np.zeros_like(X)
    cdef int i
    for i in range(ns):
        Xs[i,:] = standardize(X[i,:])
    Xs[np.isnan(Xs)] = 0
    ys = standardize(y[ix])

    cdef np.ndarray[np.int64_t, ndim=1] N = (~np.isnan(X)).sum(axis=1)
    cdef np.ndarray[np.float64_t, ndim=1] r = np.dot(Xs, ys) / N
    cdef np.ndarray[np.float64_t, ndim=1] t = r * ((N - 2) ** 0.5) / (1 - r**2)
    r[N < 3] = np.nan
    t[N < 3] = np.nan

    cdef np.ndarray[np.float64_t, ndim=1] p = scipy.stats.t.cdf(t, df=N - 2)
    p[np.isclose(r, 1) | np.isclose(r, -1)] = 0
    p = np.minimum(p, 1-p) * 2
    assert (((p <= 1) & (p >= 0)) | np.isnan(p)).all()
    cdef np.ndarray[np.float64_t, ndim=1] SLPV = -1 * np.sign(t) * np.log10(p)
    return pd.DataFrame.from_records(map(tuple, zip(N,r,p,SLPV)), 
            columns=["N","r","p","SLPV"])

cdef _spearman(np.ndarray[np.float64_t, ndim=2] X, np.ndarray[np.float64_t, ndim=1] y):
    assert X.shape[1] == y.shape[0]
    ix = ~np.isnan(y)
    assert ix.sum() >= 3
    ns = X.shape[0]
    no = ix.sum()
    X = X[:,ix]

    cdef np.ndarray[np.float64_t, ndim=1] rho = np.zeros(ns)
    rho[:] = np.nan
    cdef np.ndarray[np.int64_t, ndim=1] N = (~np.isnan(X)).sum(axis=1)

    cdef int i
    for i in range(ns):
        x = X[i,:]
        n = N[i]
        if n < 3:
            continue
        xr = wrenlab.util.ranks(x[ix]) + 1
        yr = wrenlab.util.ranks(y[ix]) + 1
        rho[i] = 1 - (6 * ((xr - yr) ** 2).sum()) / (n * (n ** 2 - 1))

    cdef np.ndarray[np.float64_t, ndim=1] F = np.arctanh(rho)
    cdef np.ndarray[np.float64_t, ndim=1] z = F * np.sqrt((N-3)/1.06)
    cdef np.ndarray[np.float64_t, ndim=1] p = scipy.stats.norm.cdf(z)
    p[np.isclose(rho, 1) | np.isclose(rho, -1)] = 0
    p = np.minimum(p, 1-p) * 2
    assert (((p <= 1) & (p >= 0)) | np.isnan(p)).all()
    cdef np.ndarray[np.float64_t, ndim=1] SLPV = -1 * np.sign(rho) * np.log10(p)
    return pd.DataFrame.from_records(map(tuple, zip(N,rho,p,SLPV)), 
            columns=["N","r","p","SLPV"])

import numpy as np
from scipy import stats, linalg

def partial_correlation(
        np.ndarray[np.float64_t, ndim=1] x,
        np.ndarray[np.float64_t, ndim=1] y,
        np.ndarray[np.float64_t, ndim=2] C):
    """
    Returns the sample linear partial correlation coefficients between x and y, 
    controlling for the variables in C.

    Parameters
    ----------
    x : np.ndarray, shape (n,)
    y : np.ndarray, shape (n,)
    C : np.ndarray, shape (n,p)

    Returns
    -------
    A tuple.

    r : float
        The partial correlation coefficient between x and y.
    p : float
        The p-value for the correlation.
    """
    n = x.shape[0]
    p = C.shape[1]

    beta_x = np.linalg.lstsq(C, x)[0]
    beta_y = np.linalg.lstsq(C, y)[0]
    res_x = x - np.dot(C, beta_x)
    res_y = y - np.dot(C, beta_y)
    r, p = scipy.stats.pearsonr(res_x, res_y)
    return r, p
    
def spearman(X, y):
    y = np.array(y)
    if isinstance(X, np.ndarray):
        return _spearman(X, y)
    elif isinstance(X, pd.DataFrame):
        Xm = np.array(X)
        o = _spearman(Xm, y)
        o.index = X.index
        o.index.name = X.index.name
        return o
    else:
        raise TypeError
    
def pearson(X, y):
    y = np.array(y)
    if isinstance(X, np.ndarray):
        return _pearson(X, y)
    elif isinstance(X, pd.DataFrame):
        Xm = np.array(X)
        o = _pearson(Xm, y)
        o.index = X.index
        o.index.name = X.index.name
        return o
    else:
        raise TypeError

def CCA(X, Y, components=5):
    """
    Run canonical correlation analysis (CCA) between X and Y,
    returning the weight matrices.
    """
    assert isinstance(X, pd.DataFrame)
    assert isinstance(Y, pd.DataFrame)
    X, Y = X.dropna(how="any").align(Y.dropna(how="any"), axis=0, join="inner")
    X = X.apply(lambda x: standardize(np.array(x)), axis=0)
    Y = Y.apply(lambda x: standardize(np.array(x)), axis=0)

    model = sklearn.cross_decomposition.CCA(n_components=components)
    model.fit(X,Y)

    def labels(n):
        return ["C{}".format(i) for i in range(1, n+1)]

    WX = pd.DataFrame(model.x_weights_, index=X.columns, columns=labels(components))
    WY = pd.DataFrame(model.y_weights_, index=Y.columns, columns=labels(components))
    return (WX, WY)

