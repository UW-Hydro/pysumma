import os
import pandas as pd
import numpy as np
import shutil
import stat
import sys
import inspect
import subprocess
from functools import partial
from pathlib import Path
from pkg_resources import resource_filename as resource
from pysumma import Simulation
from string import Template
from typing import List, Dict, Union

def read_template(path):
    with open(path, 'r') as f:
        OST_FILE= f.read()
    return Template(OST_FILE)

resource = partial(resource, __name__)

# Paths to template files
INPT_FILE = resource('meta/ostIn.template')
EXEC_FILE = resource('meta/model_executable.template')
SAVE_FILE = resource('meta/save_parameters.template')

# Templates
INPT_META = read_template(INPT_FILE)
EXEC_META = read_template(EXEC_FILE)
SAVE_META = read_template(SAVE_FILE)


class Ostrich():
    """
    Provides a high level interface to the OSTRICH optimization package.
    This class can currently only be used for single-objective optimization
    using the DDS algorithm as defined in the template file. Currently the
    metrics calculated are KGE, MAE, and MSE as defined in the evaluation
    package, though more metrics can be implemmented quite easily.

    A basic workflow for this object is:

    ::

        import pysumma as ps
        summa_exe = './summa.exe'
        ostrich_exe = './ostrich.exe'
        file_manager = './file_manager.txt'
        python_exe = '/pool0/data/andrbenn/.conda/all/bin/python'
        ostrich = ps.Ostrich(ostrich_exe, summa_exe, file_manager, python_path=python_exe)
        ostrich.calib_params = [
            ps.OstrichParam('paramName', starValue, (minValue, maxValue)),
        ]
        ostrich.obs_data_file = 'obs_data.nc'
        ostrich.sim_calib_var = 'sim_varname'
        ostrich.obs_calib_var = 'obs_varname'
        ostrich.write_config()
        ostrich.run()

    Attributes
    ----------
    ostrich:
        Path to OSTRICH executable
    python_path:
        Path to Python executable used for the ``run_script``.
        Note, you may need to set this if you are running the calibration
        from inside a non-default environment (ie from conda/poetry/etc)!
    summa:
        Path to the SUMMA executable
    template:
        OSTRICH configuration file template
    save_template:
        Template for script to save best parameters
    run_template:
        Template for script to run and evaluate SUMMA
    config_path:
        Path to location of calibration runs/logs
    simulation:
        pysumma Simulation object used as template
    file_manager:
        File manager file for SUMMA simulation
    seed:
        Random seed for calibration
    errval:
        Error value for OSTRICH
    perturb_val:
        Strength of parameter perturbations during calibration
    max_iters:
        Number of calibration trial runs
    cost_function:
        Metric to use when ranking calibration runs
    maximize:
        Whether to maximize the ``cost_function``
    simulation_kwargs:
        Keyword arguments to pass to the simulation run function
    """

    def __init__(self, ostrich_executable, summa_executable, file_manager, python_path=sys.executable):
        """Initialize a new Ostrich object"""
        self.default_metrics: np.ndarray = np.array(['KGE', 'MAE', 'MSE', 'RMSE', 'NSE'])
        self.ostrich: str = os.path.abspath(ostrich_executable)
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
        self.metrics_log: Path = self.config_path / 'metrics_log.csv'
        self.import_strings: str = ''
        self.function_strings: str = ''
        self.conversion_function: callable = lambda x: x
        self.filter_function: callable = lambda x, y: (x, y)
        self.preserve_output: str = 'no'
        self.seed: int = 42
        self.errval: float = -9999
        self.perturb_val: float = 0.2
        self.max_iters: int = 100
        self.calib_params: List[OstrichParam] = []
        self.tied_params: List[OstrichTiedParam] = []
        self.cost_function: Union[str, callable] = 'KGE'
        self.cost_function_code: str = ''
        self.objective_function: str = 'gcop'
        self.maximize: bool = True
        self.simulation_kwargs: Dict = {}
        self.allow_failures: bool = False
        self.obs_data_file: str = None
        self.sim_calib_vars: List = None
        self.obs_calib_vars: List = None

    def run(self, prerun_cmds=[], monitor=True):
        """Start calibration run"""
        if len(prerun_cmds):
            preprocess_cmd = " && ".join(prerun_cmds) + " && "
        else:
            preprocess_cmd = ""
        cmd = preprocess_cmd + f'cd {str(self.config_path)} && ./ostrich'
        self.cmd = cmd
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=True)
        if monitor:
            self.stdout, self.stderr = self.process.communicate()
            if isinstance(self.stdout, bytes):
                self.stderr = self.stderr.decode('utf-8', 'ignore')
                self.stdout = self.stdout.decode('utf-8', 'ignore')

    def test_runscript(self, prerun_cmds=[], monitor=True):
        """Run a single instance of the underlying runscript"""
        if len(prerun_cmds):
            preprocess_cmd = " && ".join(prerun_cmds) + " && "
        else:
            preprocess_cmd = ""
        cmd = preprocess_cmd + f'cd {str(self.config_path)} && ./run_script.py'
        self.cmd = cmd
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=True)
        if monitor:
            self.stdout, self.stderr = self.process.communicate()
            if isinstance(self.stdout, bytes):
                self.stderr = self.stderr.decode('utf-8', 'ignore')
                self.stdout = self.stdout.decode('utf-8', 'ignore')

    def monitor(self):
        if not self.process:
            return
        else:
            self.stdout, self.stderr = self.process.communicate()
            if isinstance(self.stdout, bytes):
                self.stderr = self.stderr.decode('utf-8', 'ignore')
                self.stdout = self.stdout.decode('utf-8', 'ignore')
        return self.stdout, self.stderr

    def write_config(self):
        """Writes all necessary files for calibration"""
        self.validate()
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
        """Write the parameter name mapping for OSTRICH"""
        with open(self.config_path / file_name, 'w') as f:
            for cp in self.calib_params:
                if cp.weightname.endswith('mtp'):
                    f.write(f'{cp.realname} | {cp.weightname}\n')
            for tp in self.tied_params:
                if tp.realname.endswith('mtp'):
                    f.write(f'{tp.realname.replace("_mtp", "")} | {tp.realname}\n')
        return Path('.') / file_name

    def write_weight_value_section(self, file_name='param_weights.txt') -> Path:
        """Write the parameter values for OSTRICH"""
        with open(self.config_path / file_name, 'w') as f:
            f.write('\n'.join([f'{cp.realname} | {cp.value}'
                               for cp in self.calib_params]) + '\n')
        return Path('.') / file_name

    def add_tied_param(self, param_name, lower_bound, upper_bound, initial_value=0.5):
        self.calib_params.append(OstrichParam(f'{param_name}', initial_value, (0.01, 0.99),
                                              weightname=f'{param_name}_scale'))
        self.tied_params.append(OstrichTiedParam(param_name, lower_bound, upper_bound))

    @property
    def param_section(self) -> str:
        """Write list of calibration parameters"""
        return '\n'.join(str(param) for param in self.calib_params)

    @property
    def tied_param_section(self) -> str:
        """Write list of tied calibration parameters"""
        if len(self.tied_params):
            return '\n'.join(str(param) for param in self.tied_params)
        else:
            return '# nothing to do here'

    @property
    def response_section(self) -> str:
        """Write section of OSTRICH configuration for selecting metric"""
        try:
            metric_row = np.argwhere(self.cost_function == self.default_metrics)[0][0]
        except IndexError:
            metric_row = -1
        return f"{self.cost_function} {self.metrics_file}; OST_NULL {metric_row} 1 ' '"

    @property
    def tied_response_section(self) -> str:
        """Write section for determining if we are maximizing or minimizing the metric"""
        if self.maximize:
            return f'neg{self.cost_function} 1 {self.cost_function} wsum -1.00'
        else:
            return '# nothing to do here'

    def open_metrics_log(self):
        columns = ['kge', 'mae', 'mse', 'rmse', 'nse']
        if self.cost_function not in columns:
            columns.append(self.cost_function)
        file = str(self.metrics_log)
        if os.path.exists(file):
            df = pd.read_csv(file, names=columns)
            return df
        else:
            #TODO: Error handling
            return None

    def open_parameter_log(self):
        file = str(self.config_path) + '/OstModel0.txt'
        if os.path.exists(file):
            df = pd.read_csv(file, delim_whitespace=True)
            return df
        else:
            #TODO: Error handling
            return None

    def validate(self):
        """Try to make sure the configuration is usable"""

        # Ensure observation data file exists
        assert os.path.isfile(self.obs_data_file), \
            (f"Observed file path doesn't exist!"
             " You specified {self.obs_data_file}")

        # Ensure the filter function has 2 args
        filter_fun_args = len(dict(inspect.signature(self.filter_function).parameters))
        assert filter_fun_args == 2, \
            (f"The filter function must have two inputs so that it can be applied",
             " to both the simulated data and the observed data!")

        # Ensure the conversion function has 1 args
        convert_fun_args = len(dict(inspect.signature(self.conversion_function).parameters))
        assert convert_fun_args == 1, \
            (f"The conversion function must have only one input so",
             " that it can be applied to the observed data!")

        # Ensure variables for calibration match up
        assert self.sim_calib_vars is not None, "sim_calib_vars cannot be None!"
        assert self.obs_calib_vars is not None, "obs_calib_vars cannot be None!"
        if type(self.sim_calib_vars) == str:
            self.sim_calib_vars = [self.sim_calib_vars]
        if type(self.obs_calib_vars) == str:
            self.obs_calib_vars = [self.obs_calib_vars]
        assert len(self.sim_calib_vars) == len(self.obs_calib_vars), \
            (f"The number of simulated calibration variables must match",
             f" the number of observed variables to compare against.",
             f" You gave {len(self.sim_calib_vars)} and",
             f" {len(self.obs_calib_vars)}, respectively")

        if callable(self.cost_function):
            self.cost_function_code = inspect.getsource(self.cost_function)
            self.cost_function = self.cost_function.__name__


    @property
    def map_vars_to_template(self):
        """For completion of the OSTRICH input template"""
        return {'runScript': self.run_script,
                'objectiveFun': self.objective_function,
                'saveScript': self.save_script,
                'preserveOutput': self.preserve_output,
                'seed': self.seed,
                'errval': self.errval,
                'perturbVal': self.perturb_val,
                'maxIters': self.max_iters,
                'paramSection': self.param_section,
                'tiedParamSection': self.tied_param_section,
                'responseSection': self.response_section,
                'tiedResponseSection': self.tied_response_section,
                'costFunction': f'neg{self.cost_function}' if self.maximize else self.cost_function,
                'weightTemplateFile': self.weightTemplateFile,
                'weightValueFile': self.weightValueFile
                }

    @property
    def map_vars_to_save_template(self):
        """For completion of the parameter saving template"""
        return {'pythonPath': self.python_path,
                'saveDir': self.config_path.parent / 'best_calibration',
                'modelDir': self.config_path}

    @property
    def map_vars_to_run_template(self):
        """For completion of the model run script template"""
        return {
                'pythonPath': self.python_path,
                'summaExe': self.summa,
                'fileManager': self.simulation.manager_path,
                'obsDataFile': os.path.abspath(self.obs_data_file),
                'simVarList': self.sim_calib_vars,
                'obsVarList': self.obs_calib_vars,
                'outFile': self.metrics_file,
                'metricsLog': self.metrics_log,
                'importStrings': self.import_strings,
                'functionStrings': self.function_strings,
                'costFunctionCode': self.cost_function_code,
                'costFunction': self.cost_function,
                'maximize': self.maximize,
                'conversionFunc': "=".join(inspect.getsource(self.conversion_function).split('=')[1:]),
                'filterFunc': "=".join(inspect.getsource(self.filter_function).split('=')[1:]),
                'paramMappingFile': self.weightTemplateFile,
                'paramWeightFile': self.weightValueFile,
                'simulationArgs': self.simulation_kwargs,
                'allowFailures': self.allow_failures,
                'paramFile': (self.simulation.manager['settingsPath'].value
                              + self.simulation.manager['trialParamFile'].value),
                }


class OstrichParam():
    """
    Definition of a SUMMA parameter to be optimized by OSTRICH

    Parameters
    ----------
    realname:
        Parameter name as seen by SUMMA
    weightname:
        Parameter name as seen by OSTRICH
    value:

        Default value
    lower:
        Lower bound for parameter value
    upper:
        Upper bound for parameter value
    """

    def __init__(self, name, value, val_range, weightname=''):
        self.realname = name
        if not weightname:
            self.weightname = f'{name}_mtp'
        else:
            self.weightname = weightname
        self.value = value
        self.lower, self.upper = val_range

    def __str__(self):
        return f"{self.weightname} {self.value} {self.lower} {self.upper} none none none free"


class OstrichTiedParam():
    def __init__(self, name, lower_param, upper_param):
        self.realname = f'{name}_mtp'
        self.weightname = f'{name}_scale'
        self.lower_param = f'{lower_param}_mtp'
        self.upper_param = f'{upper_param}_mtp'

    @property
    def type_data(self):
        """This corresponds to the equation y = x2 + x1x3 - x1x2"""
        if self.lower_param and self.upper_param:
            return "ratio 0 -1 1 0 0 1 0 0 0 0 0 0 0 0 0 1 free"
        elif self.lower_param:
            raise NotImplementedError()
            return ""
        elif self.upper_param:
            raise NotImplementedError()
            return ""

    def __str__(self):
        return f"{self.realname} 3 {self.weightname} {self.lower_param} {self.upper_param} {self.type_data}"
