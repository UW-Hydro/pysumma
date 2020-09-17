from sklearn.metrics import mean_absolute_error, mean_squared_error
import math
import numpy as np

def trim_time(sim, obs, roundto='min'):
    sim['time'] = sim['time'].dt.round(roundto)
    obs['time'] = obs['time'].dt.round(roundto)
    sim_start = sim['time'].values[1]
    sim_stop = sim['time'].values[-2]
    obs_start = obs['time'].values[1]
    obs_stop = obs['time'].values[-2]
    start = max(sim_start, obs_start)
    stop = min(sim_stop, obs_stop)
    return slice(start, stop)


def kling_gupta_efficiency(sim, obs):
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
    obs = np.asarray(obs)
    sim = np.asarray(sim)
    obs_filtered = obs[np.logical_and(~np.isnan(obs), ~np.isnan(sim))]
    sim_filtered = sim[np.logical_and(~np.isnan(obs), ~np.isnan(sim))]
    obs_mu = np.mean(obs_filtered)
    num = np.sum( (sim_filtered - obs_filtered) ** 2 )
    den = np.sum( (obs_filtered - obs_mu) ** 2 )
    return 1 - (num / den)


def root_mean_square_error(sim, obs):
    return np.sqrt(mean_squared_error(sim, obs))
