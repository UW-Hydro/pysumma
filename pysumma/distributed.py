from copy import deepcopy
from distributed import Client, get_client
from typing import List
import os
import pandas as pd
import time
import xarray as xr

from .simulation import Simulation
from .utils import ChainDict, product_dict

OMP_NUM_THREADS = int(os.environ.get('OMP_NUM_THREADS', 1))

class Distributed(object):
    '''
    Distributed objects represent SUMMA configurations where
    there are multiple GRU/HRU which are expected to be run
    in parallel.

    Currently only supports GRU based parallelization.
    '''

    def __init__(self, executable: str, filemanager: str, initialize: bool=True,
                 num_workers: int=1, threads_per_worker: int=OMP_NUM_THREADS,
                 chunk_size: int=None, num_chunks: int=None, scheduler: str=None):
        """Initialize a new distributed object"""
        self._status = 'Initialized'
        self.simulation = Simulation(executable, filemanager)
        self.submissions: list = []
        self.num_gru = self.count_gru()
        # Try to get a client, and if none exists then start a new one
        try:
            self._client = get_client()
            # Start more workers if necessary:
            workers = len(self._client.get_worker_logs())
            if workers <= self.num_workers:
                self._client.cluster.scale(workers)
        except ValueError:
            self._client = Client(n_workers=self.num_workers,
                                  threads_per_worker=threads_per_worker)
        self.chunks_args = self._gen_args(chunk_size, num_chunks)

    def _gen_args(self, chunk_size: int=None, num_chunks: int=None):
        '''
        Generate the arguments that will be used to start multiple
        runs from the base ``self.simulation``
        '''
        assert not chunk_size and num_chunks, \
            "Only specify at most one of `chunk_size` or `num_chunks`!"
        start, stop = 0, 0
        if chunk_size:
            # TODO: FIXME: implement
            chunks = [(start, stop)]
        elif num_chunks:
            # TODO: FIXME: implement
            chunks = [(start, stop)]
        else:
            # TODO: FIXME: implement
            chunks = [(start, stop)]
        return chunks


def _submit(s: Simulation, name: str, run_option: str,
            prerun_cmds: List[str], run_args: dict, **kwargs):
    s.initialize()
    s.apply_config(config)
    s.run(run_option, run_suffix=name, prerun_cmds=prerun_cmds, **run_args, **kwargs)
    s.process = None
    return s


