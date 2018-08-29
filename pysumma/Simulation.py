import subprocess
import os
import shlex

from .Decisions import Decisions
from .FileManager import FileManager


class Simulation(object):
    """The simulation object provides a wrapper for SUMMA simulations"""

    def __init__(self, executable, filemanager):
        """Initialize a new simulation object"""
        self.executable = executable
        self.manager_path = filemanager
        self.manager = FileManager(filemanager)
        decision_path = "".join([self.manager.get_value('SETTINGS_PATH'),
                                 self.manager.get_value('DECISIONS_PATH')])
        self.decisions = Decisions(decision_path)

    def execute(self, run_suffix, run_option, arglist=[]):
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
            preprocess = ['export LD_LIBRARY_PATH="{}" && '.format(
                self.library_path)]
        if arglist:
            preprocess.append('{} && '.join(arglist))
        preprocess = "".join(preprocess)
        cmd = preprocess + " && " + cmd

        # run shell script in python and print(shlex.split(cmd))
        cmd = shlex.split(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        return p
