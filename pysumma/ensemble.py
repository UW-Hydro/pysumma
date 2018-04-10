from .Simulation import simulation


class DecisionEnsemble(Ensemble):
    '''
    DecisionEnsembles represent an ensemble of SUMMA
    configurations based on chainging the decisions file.
    '''
    pass


class FileManagagerEnsemble(Ensemble):
    '''
    DecisionEnsembles represent an ensemble of SUMMA
    configurations based on chainging the decisions file.
    '''
    pass


class ParameterEnsemble(Ensemble):
    '''
    DecisionEnsembles represent an ensemble of SUMMA
    configurations based on chainging the decisions file.
    '''
    pass


class Ensemble(object):
    '''
    DecisionEnsembles represent an ensemble of SUMMA
    configurations based on chainging the decisions file.
    '''

    executable: str = None
    simulations: Simulation = []

    def __init__(self):
        pass

    def execute(self, n_workers: int=1):
        if not self.executable:
            raise Exception('No executable set!')
        raise NotImplementedError()

