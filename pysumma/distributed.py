from copy import deepcopy
from distributed import Client, get_client
from typing import List, Dict
import os
from pathlib import Path
import pandas as pd
import time
import numpy as np
import xarray as xr

from .file_manager import FileManager
from .simulation import Simulation
from .utils import ChainDict, product_dict

OMP_NUM_THREADS = int(os.environ.get('OMP_NUM_THREADS', 1))

class Distributed(object):
    '''
    Distributed objects represent SUMMA configurations where
    there are multiple GRU/HRU which are expected to be run
    in parallel.

    Currently only supports GRU based parallelization.

    Attributes
    ----------
    executable:
        Path to the SUMMA executable
    manager:
        FileManager object
    num_workers:
        Number of parallel workers to use
    chunk_args:
        List of dictionaries containing ``startGRU`` and ``countGRU`` values
    simulations:
        Dictionary of run names and Simulation objects
    '''

    def __init__(self, executable: str, filemanager: str,
                 num_workers: int=1, threads_per_worker: int=OMP_NUM_THREADS,
                 chunk_size: int=None, num_chunks: int=None, scheduler: str=None,
                 client: Client=None):
        """
        Initialize a new distributed object

        Parameters
        ----------
        executable:
            Path to the SUMMA executable
        filemanager:
            Path to the file manager
        num_workers:
            Number of workers to use for parallel runs
        threads_per_worker:
            Number of threads each worker has
        chunk_size:
            Number of GRU per job
            (cannot be used with num_chunks)
        num_chunks:
            How many jobs to split the run into
            (Cannot be used with chunk_size)
        scheduler:
            Not used currently
        """
        self._status = 'Initialized'
        self.executable = executable
        self.manager_path = Path(os.path.abspath(os.path.realpath(filemanager)))
        self.manager = FileManager(
            self.manager_path.parent, self.manager_path.name)
        self.simulations: Dict[str, Simulation] = {}
        self.submissions: List = []
        self.num_workers: int = num_workers
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
        self.chunk_args = self._generate_args(chunk_size, num_chunks)
        self._generate_simulation_objects()

    def _generate_simulation_objects(self):
        """
        Create each of the required simulation objects
        """
        for argdict in self.chunk_args:
            start = argdict['startGRU']
            stop = argdict['startGRU'] + argdict['countGRU'] - 1
            name = f"g{start}-{stop}"
            self.simulations[name] = Simulation(self.executable,
                                                self.manager_path,
                                                False)

    def _generate_args(self, chunk_size: int=None, num_chunks: int=None):
        '''
        Generate the arguments that will be used to start multiple
        runs from the base ``self.simulation``
        '''
        assert not (chunk_size and num_chunks), \
            "Only specify at most one of `chunk_size` or `num_chunks`!"
        start, stop = 0, 0
        sim_size = len(self.manager.local_attributes['gru'])
        if not (chunk_size or num_chunks):
            chunk_size = 12
        if chunk_size:
            sim_truncated = (chunk_size-1) * (sim_size // (chunk_size-1))
            starts = np.arange(1, sim_truncated+1, chunk_size).astype(int)
            stops = np.append(starts[1:], sim_size+1)
            chunks = np.vstack([starts, stops]).T
        elif num_chunks:
            chunk_size = np.ceil(sim_size / num_chunks).astype(int)
            starts = np.arange(1, sim_size, chunk_size)
            stops = np.append(starts[1:], sim_size+1)
            chunks = np.vstack([starts, stops]).T
        return [{'startGRU': start, 'countGRU': stop - start}
                for start, stop in chunks]

    def start(self, run_option: str, prerun_cmds: List=None):
        """
        Start running the ensemble members.

        Parameters
        ----------
        run_option:
            The run type. Should be either 'local' or 'docker'
        prerun_cmds:
            A list of preprocessing commands to run
        """
        for idx, (name, sim) in enumerate(self.simulations.items()):
            kwargs = self.chunk_args[idx]
            self.submissions.append(self._client.submit(
                _submit, sim, name, run_option, prerun_cmds, kwargs))

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

    def monitor(self):
        """
        Halt computation until submitted simulations are complete
        """
        simulations = self._client.gather(self.submissions)
        for s in simulations:
            self.simulations[s.run_suffix] = s

    def merge_output(self):
        pass

    def map(self, fun, args, include_sims=True, monitor=True):
        for i, (n, s) in enumerate(self.simulations.items()):
            kwargs =  self.chunk_args[i]
            if include_sims:
                all_args = (s, n, *args, kwargs)
            else:
                all_args = (*args, kwargs)
            self.submissions.append(self._client.submit(
                fun, *all_args))
        if monitor:
            return self.monitor()
        else:
            return True


def _submit(s: Simulation, name: str, run_option: str,
            prerun_cmds: List[str], run_args: dict, **kwargs):
    s.initialize()
    s.run(run_option, run_suffix=name, prerun_cmds=prerun_cmds, **run_args, **kwargs)
    s.process = None
    return s


