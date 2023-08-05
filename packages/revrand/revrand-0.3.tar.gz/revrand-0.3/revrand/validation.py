""" Some validation functions. """

from __future__ import division

import numpy as np
from scipy.stats import norm


def smse(y_true, y_predict):
    """
    Standardised mean squared error.

    Parameters
    ----------
    y_true: ndarray
        vector of true targest
    y_predict: ndarray
        vector of predicted targets

    Returns
    -------
    float:
        SMSE of predictions vs truth (scalar)

    Example
    -------
    >>> y_true = np.random.randn(100)
    >>> smse(y_true, y_true)
    0.0
    >>> smse(y_true, np.random.randn(100)) >= 1.0
    True
    """

    N = y_true.shape[0]
    return ((y_true - y_predict)**2).sum() / (N * y_true.var())


def mll(y_true, y_predict, y_var):
    """
    Mean (negative) log likelihood under a Gaussian distribution.

    Parameters
    ----------
    y_true: ndarray
        vector of true targest
    y_predict: ndarray
        vector of predicted targets
    y_var: float or ndarray
        predicted variances

    Returns
    -------
    float:
        The mean negative log likelihood

    Example
    -------
    >>> y_true = np.random.randn(100)
    >>> mean_prob = - norm.logpdf(1e-2, loc=0)  # -ve log prob close to mean
    >>> mll(y_true, y_true, 1) <= mean_prob  # Should be good predictor
    True
    >>> mll(y_true, np.random.randn(100), 1) >= mean_prob  # naive predictor
    True
    """

    return - norm.logpdf(y_true, loc=y_predict, scale=np.sqrt(y_var)).mean()


def msll(y_true, y_predict, y_var, y_train):
    """
    Mean standardised (negative) log likelihood under a Gaussian distribution.

    Parameters
    ----------
    y_true: ndarray
        vector of true targest
    y_predict: ndarray
        vector of predicted targets
    y_var: float or ndarray
        predicted variances
    y_train: ndarray
        vector of *training* targets by which to standardise

    Returns
    -------
    float:
        The negative mean standardised log likelihood

    Example
    -------
    >>> y_true = np.random.randn(100)
    >>> msll(y_true, y_true, 1, y_true) < 0  # Should be good predictor
    True
    >>> msll(y_true, np.random.randn(100), 1, y_true) >= 0  # naive predictor
    True
    """

    var = y_train.var()
    mu = y_train.mean()

    ll_naive = norm.logpdf(y_true, loc=mu, scale=np.sqrt(var))
    ll_mod = norm.logpdf(y_true, loc=y_predict, scale=np.sqrt(y_var))

    return - (ll_mod - ll_naive).mean()
