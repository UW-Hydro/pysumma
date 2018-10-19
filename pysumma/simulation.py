import subprocess
import os
import shlex

from .decisions import Decisions
from .file_manager import FileManager
from .output_control import OutputControl
from .local_param_info import LocalParamInfo


class Simulation(object):
    """The simulation object provides a wrapper for SUMMA simulations"""
    library_path = None

    def __init__(self, executable, filemanager):
        """Initialize a new simulation object"""
        self.executable = executable
        self.manager_path = filemanager
        self.manager = FileManager(filemanager)
        try:
            decision_path = "".join([self.manager.get_value('settings_path'),
                                     self.manager.get_value('decisions_path')])
            oc_path = "".join([self.manager.get_value('settings_path'),
                               self.manager.get_value('output_control')])
            lpi_path = "".join([self.manager.get_value('settings_path'),
                                self.manager.get_value('local_param_info')])
        except Exception as e:
            raise ValueError('Incorrect file manager layout - see SUMMA '
                             'documentation for guidelines') from e

        self.decisions = Decisions(decision_path)
        self.output_control = OutputControl(oc_path)
        self.local_param_info = LocalParamInfo(lpi_path)

    def start(self, run_suffix, run_option, arglist=[]):
        """Run a SUMMA simulation"""
        errstring = ('No executable defined. Set as "executable" attribute'
                     ' of Simulation or check run_option ')
        self.manager.write()
        self.decisions.write()
        self.run_suffix = run_suffix
        summa_run_cmd = "{} -p m -s {} -m {}".format(
                self.executable, self.run_suffix, self.manager_path)

        if run_option == 'local':
            cmd = summa_run_cmd
        elif run_option.startswith('docker'):

            if run_option == 'docker_latest':
                self.executable = 'bartnijssen/summa:latest'
            elif run_option == 'doocker_develop':
                self.executable = 'bartnijssen/summa:develop'
            else:
                raise ValueError(errstring)

            fman_dir = os.path.dirname(self.manager_path)
            settings_path = self.manager.get_value('SETTINGS_PATH')
            input_path = self.manager.get_value('INPUT_PATH')
            output_path = self.manager.get_value('OUTPUT_PATH')
            cmd = "".join(["docker run -v {}:{}".format(fman_dir, fman_dir),
                           " -v {}:{}".format(settings_path, settings_path),
                           " -v {}:{}".format(input_path, input_path),
                           " -v {}:{} ".format(output_path, output_path),
                           summa_run_cmd])
        else:
            raise ValueError(errstring)

        preprocess = []
        if self.library_path:
            preprocess = ['export LD_LIBRARY_PATH="{}" '.format(
                self.library_path)]
        if len(arglist):
            preprocess.append('{} && '.join(arglist))
        preprocess = "".join(preprocess)
        if len(preprocess):
            cmd = preprocess + " && " + cmd

        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=True)

    def monitor(self):
        if not self.process:
            raise RuntimeError('No simulation running! Use simulation.start '
                               'or simulation.execute to begin a simulation!')
        result = bool(self.process.wait())
        self.stdout = self.process.stdout.read().decode('utf-8')
        self.stderr = self.process.stderr.read().decode('utf-8')
        return result

    def execute(self, run_suffix, run_option, arglist=[], monitor=False):
        """Run a SUMMA simulation"""
        self.start(run_suffix, run_option, arglist)
        if monitor:
            return self.monitor()
        else:
            return self.process

