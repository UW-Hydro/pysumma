from copy import deepcopy
from distributed import Client, LocalCluster, get_client
import pandas as pd
import time
import xarray as xr

from .simulation import Simulation
from .utils import ChainDict, product_dict


class Ensemble(object):
    '''
    Ensembles represent an multiple SUMMA configurations based on
    changing the decisions or parameters of a given run.
    '''

    executable: str = None
    simulations: dict = {}
    submissions: list = []

    def __init__(self, executable: str, filemanager: str,
                 configuration: dict, num_workers: int=1):
        """
        Create a new Ensemble object. The API mirrors that of the
        Simulation object.
        """
        self._status = 'Initialized'
        self.executable = executable
        self.filemanager = filemanager
        self.configuration = configuration
        self.num_workers = num_workers
        # Try to get a client, and if none exists then start a new one
        try:
            self._client = get_client()
            # Start more workers if necessary
            workers = len(self._client.get_worker_logs())
            if workers < self.num_workers:
                self._client.cluster.scale_up(self.num_workers)
        except ValueError:
            self._client = Client(n_workers=num_workers, threads_per_worker=1)
        self._generate_simulation_objects()

    def _generate_simulation_objects(self):
        """
        Create a mapping of configurations to the simulation objects.
        """
        for name, config in self.configuration.items():
            s = Simulation(self.executable, self.filemanager)
            for k, v in config.get('decisions', {}).items():
                s.decisions.set_option(k, v)
            for k, v in config.get('file_manager', {}).items():
                s.manager.set_option(k, v)
            for k, v in config.get('force_files', {}).items():
                s.manager.set_option(k, v)
            for k, v in config.get('parameters', {}).items():
                s.local_param_info.set_option(k, v)
            self.simulations[name] = s

    def _generate_coords(self):
        """
        Generate the coordinates that can be used to merge the output
        of the ensemble runs into a single dataset.
        """
        decision_dims = ChainDict()
        manager_dims = ChainDict()
        parameter_dims = ChainDict()
        for name, conf in self.configuration.items():
            for k, v in conf.get('decisions', {}).items():
                decision_dims[k] = v
            for k, v in conf.get('file_manager', {}).items():
                manager_dims[k] = v
            for k, v in conf.get('parameters', {}).items():
                parameter_dims[k] = v
        return {'decisions': decision_dims,
                'managers': manager_dims,
                'parameters': parameter_dims}

    def merge_output(self):
        """
        Open and merge all of the output datasets from the ensemble
        run into a single dataset.
        """
        nc = self._generate_coords()
        new_coords = (list(nc.get('decisions', {}))
                      + list(nc.get('parameters', {})))
        decision_tuples = [tuple(n.split('++')[1:-1])
                           for n in self.configuration.keys()]
        for i, t in enumerate(decision_tuples):
            decision_tuples[i] = tuple((float(l.split('=')[-1])
                                        if '=' in l else l for l in t))
        decision_names = ['++'.join(tuple(n.split('++')[1:-1]))
                          for n in self.configuration.keys()]
        for i, t in enumerate(decision_names):
            decision_names[i] = '++'.join(l.split('=')[0] for l in t)
        new_idx = pd.MultiIndex.from_tuples(
            decision_tuples, names=new_coords)
        out_file_paths = [s._get_output() for s in self.simulations.values()]
        out_file_paths = [fi for sublist in out_file_paths for fi in sublist]
        full = xr.open_mfdataset(out_file_paths, concat_dim='run_number')
        merged = full.assign_coords(run_number=decision_names)
        merged['run_number'] = new_idx
        merged = merged.unstack('run_number')
        return merged

    def start(self, run_option: str, arg_list: list=[], monitor: bool=False):
        """
        Start running the ensemble members.

        Parameters
        ----------
        run_option:
            The run type. Should be either 'local' or 'docker'
        arg_list:
            A list of preprocessing commands to run
        monitor:
            Whether or not to halt computation until the runs are complete
        """
        for n, s in self.simulations.items():
            # Sleep calls are to ensure writeout happens
            time.sleep(1.5)
            self.submissions.append(self._client.submit(
                _submit, s, n, run_option, arg_list))
            time.sleep(1.5)
        if monitor:
            return self.monitor()

    def monitor(self):
        """
        Halt computation until submitted simulations are complete
        """
        simulations = self._client.gather(self.submissions)
        for s in simulations:
            self.simulations[s.run_suffix] = s


def _submit(s: Simulation, name: str, run_option: str, arg_list):
    s.execute(run_option, run_suffix=name,
              monitor=True, preprocess_cmds=arg_list)
    return s


def decision_product(list_config):
    return {'++'+'++'.join(d.values())+'++': {'decisions': d}
            for d in product_dict(**list_config)}


def parameter_product(list_config):
    return {'++'+'++'.join('{}={}'.format(k, v) for k, v in d.items())+'++':
            {'parameters': d} for d in product_dict(**list_config)}


def total_product(dec_conf={}, param_conf={}):
    full_conf = deepcopy(dec_conf)
    full_conf.update(param_conf)
    prod_dict = product_dict(**full_conf)
    config = {}
    for d in prod_dict:
        name = '++' + '++'.join(
            '{}={}'.format(k, v) if k in param_conf else v
            for k, v in d.items()) + '++'
        config[name] = {'decisions': {}, 'parameters': {}}
        for k, v in d.items():
            if k in dec_conf:
                config[name]['decisions'][k] = v
            elif k in param_conf:
                config[name]['parameters'][k] = v
    return config
