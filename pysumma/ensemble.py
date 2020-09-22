from copy import deepcopy
from distributed import Client, get_client
import os
import pandas as pd
import time
import xarray as xr

from .simulation import Simulation
from .utils import ChainDict, product_dict

OMP_NUM_THREADS = int(os.environ.get('OMP_NUM_THREADS', 1))


class Ensemble(object):
    '''
    Ensembles represent an multiple SUMMA configurations based on
    changing the decisions or parameters of a given run.

    Attributes
    ----------
    executable:
        Path to the SUMMA executable
    filemanager: (optional)
        Path to the file manager
    configuration:
        Dictionary of runs, along with settings
    num_workers:
        Number of parallel workers to use
    simulations:
        Dictionary of run names and Simulation objects
    '''

    def __init__(self, executable: str,configuration: dict,
                 filemanager: str=None, num_workers: int=1,
                 threads_per_worker: int=OMP_NUM_THREADS,
                 scheduler: str=None, client: Client=None):
        """
        Create a new Ensemble object. The API mirrors that of the
        Simulation object.
        """
        self._status = 'Initialized'
        self.executable: str = executable
        self.filemanager: str = filemanager
        self.configuration: dict = configuration
        self.num_workers: int = num_workers
        self.simulations: dict = {}
        self.submissions: list = []
        # Try to get a client, and if none exists then start a new one
        if client:
            self._client = client
            workers = len(self._client.get_worker_logs())
            if workers <= self.num_workers:
                self._client.cluster.scale(workers)
        else:
            try:
                self._client = get_client()
                # Start more workers if necessary:
                workers = len(self._client.get_worker_logs())
                if workers <= self.num_workers:
                    self._client.cluster.scale(workers)
            except ValueError:
                self._client = Client(n_workers=self.num_workers,
                                      threads_per_worker=threads_per_worker)
        self._generate_simulation_objects()

    def _generate_simulation_objects(self):
        """
        Create a mapping of configurations to the simulation objects.
        """
        if self.filemanager:
            for name, config in self.configuration.items():
                self.simulations[name] = Simulation(
                    self.executable, self.filemanager, False)
        else:
            for name, config in self.configuration.items():
                assert config['file_manager'] is not None, \
                    "No filemanager found in configuration or Ensemble!"
                self.simulations[name] = Simulation(
                    self.executable, config['file_manager'], False)

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
            #for k, v in conf.get('parameters', {}).items():
            #    parameter_dims[k] = v
            for k, v in conf.get('trial_parameters', {}).items():
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
        if sum([len(dt) for dt in decision_tuples]) == 0:
            raise NameError("Simulations in the ensemble do not share all"
                            " common decisions! Please use `open_output`"
                            " to retrieve the output of this Ensemble")
        for i, t in enumerate(decision_names):
            decision_names[i] = '++'.join(l.split('=')[0] for l in t)
        new_idx = pd.MultiIndex.from_tuples(
            decision_tuples, names=new_coords)
        out_file_paths = [s.get_output_files() for s in self.simulations.values()]
        out_file_paths = [fi for sublist in out_file_paths for fi in sublist]
        full = xr.open_mfdataset(out_file_paths, concat_dim='run_number', combine='nested')
        merged = full.assign_coords(run_number=decision_names)
        merged['run_number'] = new_idx
        merged = merged.unstack('run_number')
        return merged

    def start(self, run_option: str, prerun_cmds: list=None):
        """
        Start running the ensemble members.

        Parameters
        ----------
        run_option:
            The run type. Should be either 'local' or 'docker'
        prerun_cmds:
            A list of preprocessing commands to run
        """
        for n, s in self.simulations.items():
            # Sleep calls are to ensure writeout happens
            config = self.configuration[n]
            self.submissions.append(self._client.submit(
                _submit, s, n, run_option, prerun_cmds, config))

    def run(self, run_option: str, prerun_cmds=None, monitor: bool=True):
        """
        Run the ensemble

        Parameters
        ----------
        run_option:
            Where to run the simulation. Can be ``local`` or ``docker``
        prerun_cmds:
            A list of shell commands to run before running SUMMA
        monitor:
            Whether to halt operation until runs are complete
        """
        self.start(run_option, prerun_cmds)
        if monitor:
            return self.monitor()
        else:
            return True

    def map(self, fun, args, include_sims=True, monitor=True):
        for n, s in self.simulations.items():
            config = self.configuration[n]
            if include_sims:
                all_args = (s, n, *args, {'config': config})
            else:
                all_args = (*args, {'config': config})
            self.submissions.append(self._client.submit(
                fun, *all_args))
        if monitor:
            return self.monitor()
        else:
            return True

    def monitor(self):
        """
        Halt computation until submitted simulations are complete
        """
        simulations = self._client.gather(self.submissions)
        for s in simulations:
            self.simulations[s.run_suffix] = s

    def summary(self):
        """
        Show the user information about ensemble status
        """
        success, error, other = [], [], []
        for n, s in self.simulations.items():
            if s.status == 'Success':
                success.append(n)
            elif s.status == 'Error':
                error.append(n)
            else:
                other.append(n)
        return {'success': success, 'error': error, 'other': other}

    def rerun_failed(self, run_option: str, prerun_cmds=None,
                     monitor: bool=True):
        """
        Try to re-run failed simulations.

        Parameters
        ----------
        run_option:
            Where to run the simulation. Can be ``local`` or ``docker``
        prerun_cmds:
            A list of shell commands to run before running SUMMA
        monitor:
            Whether to halt operation until runs are complete
        """
        run_summary = self.summary()
        self.submissions = []
        for n in run_summary['error']:
            config = self.configuration[n]
            s = self.simulations[n]
            s.reset()
            self.submissions.append(self._client.submit(
                _submit, s, n, run_option, prerun_cmds, config))
        if monitor:
            return self.monitor()
        else:
            return True


def _submit(s: Simulation, name: str, run_option: str, prerun_cmds, config):
    s.initialize()
    s.apply_config(config)
    s.run(run_option, run_suffix=name, prerun_cmds=prerun_cmds)
    s.process = None
    return s


def decision_product(list_config):
    """
    Create a dictionary of runs based on a simpler list configuration
    of decision options

    Parameters
    ----------
    list_config:
        A dictionary of the sort
        {key1: [list of values], key2: [list of values]}

    Returns
    --------
    A dictionary of the sort:
        {name: {key1: value1, key2: value1},
         name: {key1: value2, key2: value1},
         ...
         name: {key1: valueN, key2: valueN}}
    """
    return {'++'+'++'.join(d.values())+'++': {'decisions': d}
            for d in product_dict(**list_config)}


def parameter_product(list_config):
    """
    Create a dictionary of runs based on a simpler list configuration
    of parameter values

    Parameters
    ----------
    list_config:
        A dictionary of the sort
        {key1: [list of values], key2: [list of values]}

    Returns
    --------
    A dictionary of the sort:
        {name: {key1: value1, key2: value1},
         name: {key1: value2, key2: value1},
         ...
         name: {key1: valueN, key2: valueN}}
    """
    return {'++'+'++'.join('{}={}'.format(k, v) for k, v in d.items())+'++':
            {'parameters': d} for d in product_dict(**list_config)}


def attribute_product(list_config):
    """
    Create a dictionary of runs based on a simpler list configuration
    of attribute values

    Parameters
    ----------
    list_config:
        A dictionary of the sort
        {key1: [list of values], key2: [list of values]}

    Returns
    --------
    A dictionary of the sort:
        {name: {key1: value1, key2: value1},
         name: {key1: value2, key2: value1},
         ...
         name: {key1: valueN, key2: valueN}}
    """
    return {'++'+'++'.join('{}={}'.format(k, v) for k, v in d.items())+'++':
            {'attributes': d} for d in product_dict(**list_config)}


def trial_parameter_product(list_config):
    """
    Create a dictionary of runs based on a simpler list configuration
    of trial parameter values

    Parameters
    ----------
    list_config:
        A dictionary of the sort
        {key1: [list of values], key2: [list of values]}

    Returns
    --------
    A dictionary of the sort:
        {name: {key1: value1, key2: value1},
         name: {key1: value2, key2: value1},
         ...
         name: {key1: valueN, key2: valueN}}
    """
    return {'++'+'++'.join('{}={}'.format(k, v) for k, v in d.items())+'++':
            {'trial_parameters': d} for d in product_dict(**list_config)}



def file_manager_product(list_config):
    """
    Create a dictionary of runs based on a simpler list configuration
    of file managers

    Parameters
    ----------
    list_config:
        A dictionary of the sort
        {key1: [list of values], key2: [list of values]}

    Returns
    --------
    A dictionary of the sort:
        {name: {key1: value1, key2: value1},
         name: {key1: value2, key2: value1},
         ...
         name: {key1: valueN, key2: valueN}}
    """
    return {'++'+'++'.join('{}={}'.format(k, v) for k, v in d.items())+'++':
            {'file_manager': d} for d in product_dict(**list_config)}


def total_product(dec_conf={}, param_conf={}, attr_conf={}, fman_conf={},
                  param_trial_conf={}, sequential_keys=False):
    """
    Combines multiple types of model changes into a single configuration
    for the Ensemble object.
    """
    full_conf = deepcopy(dec_conf)
    full_conf.update(param_conf)
    full_conf.update(attr_conf)
    full_conf.update(param_trial_conf)
    full_conf.update(fman_conf)
    prod_dict = product_dict(**full_conf)
    config = {}
    for i, d in enumerate(prod_dict):
        name = '++' + '++'.join(
            '{}={}'.format(k, v) if k in param_conf or k in attr_conf or k in param_trial_conf
            else v.replace('/', '_').replace('\\', '_')
            for k, v in d.items()) + '++'
        if sequential_keys:
            name = f'run_{i}'
        config[name] = {'decisions': {}, 'parameters': {}, 'attributes': {}, 'trial_parameters': {}}
        for k, v in d.items():
            if k in dec_conf:
                config[name]['decisions'][k] = v
            elif k in param_conf:
                config[name]['parameters'][k] = v
            elif k in attr_conf:
                config[name]['attributes'][k] = v
            elif k in param_trial_conf:
                config[name]['trial_parameters'][k] = v
            elif k in fman_conf:
                config[name]['file_manager'] = v
    return config
