from pkg_resources import resource_filename as resource
from functools import partial
from string import Template
from typing import List, Dict

def read_template(path):
    with open(path, 'r') as f:
        OST_FILE= f.read()
    return Template(OST_FILE)

resource = partial(resource, __name__)

INPT_META = read_template(resource('meta/ostIn.template'))
EXEC_META = read_template(resource('meta/model_executable.template'))
LOSS_META = read_template(resource('meta/objective_function.template'))
SAVE_META = read_template(resource('meta/save_parameters.template'))


class Ostrich():

    def __init__(self, ostrich_executable, summa_executable):
        self.ostrich: str = ostrich_executable
        self.summa: str = summa_executable
        self.template: Template = INPT_META
        self.preserve_output: str ='no'
        self.seed: int = 42
        self.errval: float = -9999
        self.perturb_val: float = 0.2
        self.max_iters: int = 100
        self.calib_params: List[OstrichParam] = []
        self.cost_function = 'KGE'
        self.maximize = True

    def read_config(self, config_file):
        raise NotImplementedError()

    def write_config(self, path):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def to_simulation(self):
        raise NotImplementedError()

    def save_setup(self, path):
        raise NotImplementedError()

    @property
    def param_section(self) -> str:
        return '\n'.join(str(param) for param in self.calib_params)

    def write_weight_template_section(self, path='./param_mapping.tpl') -> str:
        with open(path) as f:
            f.write('\n'.join([f'{cp.realname} | {cp.weightname}'
                               for cp in self.calib_params]))
        return path

    def write_weight_value_section(self, path='./param_weights.txt') -> str:
        with open(path) as f:
            f.write('\n'.join([f'{cp.realname} | {cp.value}'
                               for cp in self.calib_params]))
        return path

    @property
    def tied_response_section(self) -> str:
        if self.maximize:
            return f'neg{self.cost_function} 1 {self.cost_function} wsum -1.0.0'
        else:
            return '# nothing to do here'

    @property
    def map_vars_to_template(self) -> Dict[str: str]:
        return {'runScript': self.run_script,
                'objectiveFun': self.objective_function,
                'saveScript': self.save_script,
                'preserveOutput': self.preserve_output,
                'seed': self.seed,
                'errval': self.errval,
                'perturbVal': self.perturb_val,
                'maxIters': self.max_iters,
                'paramSection': self.param_section,
                'responseSection': self.response_section,
                'tiedResponseSection': self.tied_response_section,
                'costFunction': self.cost_function
                }

class OstrichParam():

    def __init__(self, name, value, val_range):
        self.realname = name
        self.weightname = f'{name}_mtp'
        self.value = value
        self.lower, self.upper = val_range

    def __str__(self):
        return f"{self.weightname} {self.value} {self.lower} none none none free"
