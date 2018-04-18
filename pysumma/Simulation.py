
import subprocess


class Simulation(object):
    def __init__(self, file_manager_path):
        self.file_manager = FileManager(file_manager_path)
        self.decisions = Decisions(self.file_manager.decisions_file)
        self.output_control = OutputControl(self.file_manager.output_control)

    def execute(self, run_suffix, run_option):
        self.run_suffix = run_suffix
        if run_option == 'local':
            cmd = "{} -p never -s {} -m {}".format(self.executable,
                                                   self.run_suffix,
                                                   self.filepath)

        elif run_option == "docker_latest":
            self.executable = 'bartnijssen/summa:latest'
            cmd = "docker run -v {}:{}".format(self.file_dir,
                                               self.file_dir) + \
                  " -v {}:{}".format(self.setting_path.filepath,
                                     self.setting_path.filepath) + \
                  " -v {}:{}".format(self.input_path.filepath,
                                     self.input_path.filepath) + \
                  " -v {}:{}".format(self.output_path.filepath,
                                     self.output_path.filepath) + \
                  " {} -p never -s {} -m {}".format(self.executable,
                                                    self.run_suffix,
                                                    self.filepath)

        elif run_option == "docker_develop":
            self.executable = 'bartnijssen/summa:develop'
            cmd = "docker run -v {}:{}".format(self.file_dir,
                                               self.file_dir) + \
                  " -v {}:{}".format(self.setting_path.filepath,
                                     self.setting_path.filepath) + \
                  " -v {}:{}".format(self.input_path.filepath,
                                     self.input_path.filepath) + \
                  " -v {}:{}".format(self.output_path.filepath,
                                     self.output_path.filepath) + \
                  " {} -p never -s {} -m {}".format(self.executable,
                                                    self.run_suffix,
                                                    self.filepath)

        else:
            raise ValueError('No executable defined. Set as'
                             '"executable" attribute of Simulation'
                             'or check run_option')
        # run shell script in python
        if self.library_path:
            libstr = 'export LD_LIBRARY_PATH="{}";'.format(self.library_path)
            cmd = "".join([libstr, cmd])
        proc = subprocess.Popen(cmd, shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        # define output file name
        self.output_file = "".join([self.output_path.filepath,
                                    self.output_prefix.value + 'output_',
                                    self.run_suffix + '_timestep.nc'])
        return proc

    def run_local(self, **kwargs):
        pass

    def run_docker(self, **kwargs):
        pass

    def run_remote(self, **kwargs):
        raise NotImplementedError()


class FileManager(object):

    fman_opts = ['header', 'settings_path', 'input_path', 'output_path',
                 'decisions_path', 'meta_time', 'meta_attr', 'meta_type',
                 'meta_force', 'meta_local_param', 'output_control',
                 'meta_local_idx', 'meta_basin_param', 'meta_basin_var',
                 'local_attr', 'local_param_info', 'basin_param_info',
                 'force_file_list', 'model_init_cond', 'param_trial',
                 'output_prefix']
    original_file_contents = None
    original_path = None
    overwrite_lines = []

    def __init__(self, path):
        self.original_path = path
        self.read(path)

    def read(self, path):
        with open(path, 'r') as f:
            self.original_contents = f.readlines()
        opt_count = 0
        attrs = {}
        for linum, line in enumerate(self.original_contents):
            if not line.startswith('!'):
                attrs[self.fman_opts[opt_count]] = line.split('!')[0].strip()
                opt_count += 1
                self.overwrite_lines.append(linum)
        assert opt_count == len(self.fman_opts)
        self.__dict__.update(attrs)

    def write(self, path=None):
        assert self.original_file_contents is not None
        if not path:
            path = self.original_path
        opt_count = 0
        self.new_contents = []
        for linum, line in enumerate(self.original_contents):
            if linum in self.overwrite_lines:
                oldval = line.split('!')[0].strip()
                newval = self.__dict__[self.fman_opts[opt_count]]
                line = line.replace(oldval, newval)
                opt_count += 1
            self.new_contents.append(line)
        assert opt_count == len(self.overwrite_lines)
        with open(path, 'w') as f:
            for line in self.new_contents:
                f.write(line)


class Decisions(object):

    def __init__(self, path):
        pass

    def read(self, path):
        pass

    def write(self, path):
        pass


class OutputControl(object):

    def __init__(self, path):
        pass

    def read(self, path):
        pass

    def write(self, path):
        pass


class BasinParameters(object):

    def __init__(self, path):
        pass

    def read(self, path):
        pass

    def write(self, path):
        pass


class LocalParameters(object):

    def __init__(self, path):
        pass

    def read(self, path):
        pass

    def write(self, path):
        pass
