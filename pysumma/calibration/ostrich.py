from pkg_resources import resource_filename as resource
from functools import partial
from string import Template
from typing import List, Dict
from pathlib import Path
from pysumma import Simulation
import subprocess
import shutil
import stat
import os

def read_template(path):
    with open(path, 'r') as f:
        OST_FILE= f.read()
    return Template(OST_FILE)

resource = partial(resource, __name__)

INPT_FILE = resource('meta/ostIn.template')
EXEC_FILE = resource('meta/model_executable.template')
SAVE_FILE = resource('meta/save_parameters.template')

INPT_META = read_template(INPT_FILE)
EXEC_META = read_template(EXEC_FILE)
SAVE_META = read_template(SAVE_FILE)


class Ostrich():

    def __init__(self, ostrich_executable, summa_executable, file_manager, python_path='python'):
        self.ostrich: str = ostrich_executable
        self.python_path: str = python_path
        self.summa: str = summa_executable
        self.template: Template = INPT_META
        self.save_template: Template = SAVE_META
        self.run_template: Template = EXEC_META
        self.config_path: Path = Path(os.path.abspath(file_manager)).parent / 'calibration'
        self.simulation = Simulation(summa_executable, file_manager,
                                     config_dir=self.config_path)
        self.file_manager = self.simulation.manager
        self.run_script: Path = self.config_path / 'run_script.py'
        self.save_script: Path = self.config_path / 'save_script.py'
        self.metrics_file: Path = self.config_path / 'metrics.txt'
        self.preserve_output: str ='no'
        self.seed: int = 42
        self.errval: float = -9999
        self.perturb_val: float = 0.2
        self.max_iters: int = 100
        self.calib_params: List[OstrichParam] = []
        self.cost_function: str = 'KGE'
        self.objective_function: str = 'gcop'
        self.maximize: bool = True

    def run(self, prerun_cmds=[]):
        if len(prerun_cmds):
            preprocess_cmd = " && ".join(prerun_cmds) + " && "
        else:
            preprocess_cmd = ""
        cmd = preprocess_cmd + f'cd {str(self.config_path)} && ./ostrich'
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=True)
        self.stdout, self.stderr = self.process.communicate()
        if isinstance(self.stdout, bytes):
            self.stderr = self.stderr.decode('utf-8', 'ignore')
            self.stdout = self.stdout.decode('utf-8', 'ignore')

    def read_config(self, config_file):
        raise NotImplementedError('We do not yet support importing OSTRICH configurations!')

    def write_config(self):
        if not os.path.exists(self.config_path):
            os.mkdir(self.config_path)

        # Substitue templates and save
        self.weightTemplateFile = self.write_weight_template_section()
        self.weightValueFile = self.write_weight_value_section()

        with open(self.config_path / 'ostIn.txt', 'w') as f:
            f.write(self.template.substitute(self.map_vars_to_template))
        with open(self.save_script, 'w') as f:
            f.write(self.save_template.substitute(self.map_vars_to_save_template))

        self.simulation._write_configuration()
        with open(self.run_script, 'w') as f:
            f.write(self.run_template.substitute(self.map_vars_to_run_template))

        shutil.copy(self.ostrich, self.config_path / 'ostrich')

        # Make sure we set permissions for execution
        st = os.stat(self.config_path / 'ostrich')
        os.chmod(self.config_path / 'ostrich', st.st_mode | stat.S_IEXEC)
        st = os.stat(self.run_script)
        os.chmod(self.run_script, st.st_mode | stat.S_IEXEC)
        st = os.stat(self.save_script)
        os.chmod(self.save_script, st.st_mode | stat.S_IEXEC)

    def write_weight_template_section(self, file_name=Path('param_mapping.tpl')) -> Path:
        with open(self.config_path / file_name, 'w') as f:
            f.write('\n'.join([f'{cp.realname} | {cp.weightname}'
                               for cp in self.calib_params]))
        return Path('.') / file_name

    def write_weight_value_section(self, file_name='param_weights.txt') -> Path:
        with open(self.config_path / file_name, 'w') as f:
            f.write('\n'.join([f'{cp.realname} | {cp.value}'
                               for cp in self.calib_params]))
        return Path('.') / file_name

    @property
    def param_section(self) -> str:
        return '\n'.join(str(param) for param in self.calib_params)

    @property
    def response_section(self) -> str:
        return f"{self.cost_function} {self.metrics_file}; OST_NULL 0 1 ' '"

    @property
    def tied_response_section(self) -> str:
        if self.maximize:
            return f'neg{self.cost_function} 1 {self.cost_function} wsum -1.00'
        else:
            return '# nothing to do here'

    @property
    def map_vars_to_template(self):
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
                'costFunction': f'neg{self.cost_function}' if self.maximize else self.cost_function,
                'weightTemplateFile': self.weightTemplateFile,
                'weightValueFile': self.weightValueFile
                }

    @property
    def map_vars_to_save_template(self):
        return {
                'pythonPath': self.python_path,
                'saveDir': self.config_path.parent / 'best_calibration',
                'modelDir': self.config_path}

    @property
    def map_vars_to_run_template(self):
        return {
                'pythonPath': self.python_path,
                'summaExe': self.summa,
                'fileManager': self.simulation.manager_path,
                'obsDataFile': self.obs_data_file,
                'simVarName': self.sim_calib_var,
                'obsVarName': self.obs_calib_var,
                'outFile': self.metrics_file,
                'paramMappingFile': self.weightTemplateFile,
                'paramWeightFile': self.weightValueFile,
                'paramFile': (self.simulation.manager['settings_path'].value
                              + self.simulation.manager['parameter_trial'].value),
                }


class OstrichParam():

    def __init__(self, name, value, val_range):
        self.realname = name
        self.weightname = f'{name}_mtp'
        self.value = value
        self.lower, self.upper = val_range

    def __str__(self):
        return f"{self.weightname} {self.value} {self.lower} {self.upper} none none none free"


def read_ostrich_params(path):
    pass
