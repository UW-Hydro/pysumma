from sklearn.metrics import mean_absolute_error, mean_squared_error
import math
import numpy as np


def kling_gupta_efficiency(sim, obs):
    obs = np.asarray(obs)
    sim = np.asarray(sim)
    obs_filtered = obs[~np.isnan(obs)]
    sim_filtered = sim[~np.isnan(obs)]
    sim_std = np.std(sim_filtered, ddof=1)
    obs_std = np.std(obs_filtered, ddof=1)
    sim_mu = np.mean(sim_filtered)
    obs_mu = np.mean(obs_filtered)
    r = np.corrcoef(sim_filtered, obs_filtered)[0, 1]
    var = sim_std / obs_std
    bias = sim_mu / obs_mu
    kge = 1 - np.sqrt((bias-1)**2 + (var-1)**2 + (r-1)**2)
    return kge


def root_mean_square_error(sim, obs):
    return np.sqrt(mean_squared_error(sim, obs))
