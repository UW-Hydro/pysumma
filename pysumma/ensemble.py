from typing import List

from .Simulation import Simulation


class Ensemble(object):
    '''
    DecisionEnsembles represent an ensemble of SUMMA
    configurations based on chainging the decisions file.
    '''

    executable: str = None
    simulations: List[Simulation] = []

    def __init__(self):
        pass

    def execute(self, n_workers: int=1):
        if not self.executable:
            raise Exception('No executable set!')
        raise NotImplementedError()

    def status(self):
        tot = len(self.simulations)
        queued = 0  # sum([s.proc is None for s in self.simulations])
        running = 0  # sum([s.proc.poll() is None for s in self.simulations])
        return {'total jobs': tot,
                'queued jobs': queued,
                'running jobs': running,
                'completed jobs': tot - queued - running,
                'failed jobs': 'not implemented'}


class DecisionEnsemble(Ensemble):
    '''
    DecisionEnsembles represent an ensemble of SUMMA
    configurations based on changing the decisions file.
    '''
    def __init__(self):
        raise NotImplementedError()


class FileManagagerEnsemble(Ensemble):
    '''
    DecisionEnsembles represent an ensemble of SUMMA
    configurations based on changing the decisions file.
    '''
    def __init__(self):
        raise NotImplementedError()


class ParameterEnsemble(Ensemble):
    '''
    DecisionEnsembles represent an ensemble of SUMMA
    configurations based on changing the decisions file.
    '''
    def __init__(self):
        raise NotImplementedError()
