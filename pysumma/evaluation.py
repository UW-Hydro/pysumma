from sklearn.metrics import mean_absolute_error, mean_squared_error
import math
import numpy as np

def trim_time(ds1, ds2, roundto='min'):
    """
    Match the time length between two datasets.

    Parameters
    ----------
    ds1: xr.Dataset
        First dataset to trim time with
    ds2: xr.Dataset
        Second dataset to trim time with
    roundto: str, optional, default='min'
        Time frequency to round the time vector to
        This can help match up timseries if there are
        small differences

    Returns
    -------
    A time slice with the longest overlap between
    the two input datasets
    """
    ds1['time'] = ds1['time'].dt.round(roundto)
    ds2['time'] = ds2['time'].dt.round(roundto)
    ds1_start = ds1['time'].values[1]
    ds1_stop = ds1['time'].values[-2]
    ds2_start = ds2['time'].values[1]
    ds2_stop = ds2['time'].values[-2]
    start = max(ds1_start, ds2_start)
    stop = min(ds1_stop, ds2_stop)
    return slice(start, stop)


def kling_gupta_efficiency(sim, obs):
    """
    Calculates the KGE

    Parameters
    ----------
    sim: xr.DataArray
        Model output variable
    obs: xr.DataArray
        Variable representing observations/references

    Returns
    -------
    The KGE score
    """
    obs = np.asarray(obs)
    sim = np.asarray(sim)
    obs_filtered = obs[np.logical_and(~np.isnan(obs), ~np.isnan(sim))]
    sim_filtered = sim[np.logical_and(~np.isnan(obs), ~np.isnan(sim))]
    sim_std = np.std(sim_filtered, ddof=1)
    obs_std = np.std(obs_filtered, ddof=1)
    sim_mu = np.mean(sim_filtered)
    obs_mu = np.mean(obs_filtered)
    r = np.corrcoef(sim_filtered, obs_filtered)[0, 1]
    var = sim_std / obs_std
    bias = sim_mu / obs_mu
    kge = 1 - np.sqrt((bias-1)**2 + (var-1)**2 + (r-1)**2)
    return kge


def decomposed_kling_gupta_efficiency(sim, obs):
    """
    Calculates the KGE

    Parameters
    ----------
    sim: xr.DataArray
        Model output variable
    obs: xr.DataArray
        Variable representing observations/references

    Returns
    -------
    The components of the KGE score, as
    kge, bias, variance, correlation
    """
    obs = np.asarray(obs)
    sim = np.asarray(sim)
    obs_filtered = obs[np.logical_and(~np.isnan(obs), ~np.isnan(sim))]
    sim_filtered = sim[np.logical_and(~np.isnan(obs), ~np.isnan(sim))]
    sim_std = np.std(sim_filtered, ddof=1)
    obs_std = np.std(obs_filtered, ddof=1)
    sim_mu = np.mean(sim_filtered)
    obs_mu = np.mean(obs_filtered)
    r = np.corrcoef(sim_filtered, obs_filtered)[0, 1]
    var = sim_std / obs_std
    bias = sim_mu / obs_mu
    kge = 1 - np.sqrt((bias-1)**2 + (var-1)**2 + (r-1)**2)
    return kge, bias, var, r


def nash_sutcliffe_efficiency(sim, obs):
    """
    Calculates the NSE

    Parameters
    ----------
    sim: xr.DataArray
        Model output variable
    obs: xr.DataArray
        Variable representing observations/references

    Returns
    -------
    The NSE score
    """
    obs = np.asarray(obs)
    sim = np.asarray(sim)
    obs_filtered = obs[np.logical_and(~np.isnan(obs), ~np.isnan(sim))]
    sim_filtered = sim[np.logical_and(~np.isnan(obs), ~np.isnan(sim))]
    obs_mu = np.mean(obs_filtered)
    num = np.sum( (sim_filtered - obs_filtered) ** 2 )
    den = np.sum( (obs_filtered - obs_mu) ** 2 )
    return 1 - (num / den)


def root_mean_square_error(sim, obs):
    """
    Calculates the RMSE

    Parameters
    ----------
    sim: xr.DataArray
        Model output variable
    obs: xr.DataArray
        Variable representing observations/references

    Returns
    -------
    RMSE between the sim and obs variables
    """
    return np.sqrt(mean_squared_error(sim, obs))
