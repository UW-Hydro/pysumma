import copy


class LocalParamInfo(object):

    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.original_contents = f.readlines()
        self.new_contents = copy.deepcopy(self.original_contents)

    def replace(self, key, default, low, uppr):
        for i, ln in enumerate(self.new_contents):
            if ln.startswith(key):
                self.new_contents[i] = (
                        "{:25s} | {:>12.4f} | {:>12.4f} | {:>12.4f}\n"
                        .format(key, default, low, uppr))
        with open(self.filepath, 'w') as f:
            f.writelines(self.new_contents)

    def restore(self):
        with open(self.filepath, 'w') as f:
            f.writelines(self.original_contents)
        with open(self.filepath, 'r') as f:
            self.original_contents = f.readlines()
        self.new_contents = copy.deepcopy(self.original_contents)

    def __repr__(self):
        return '\n'.join(self.new_contents)
