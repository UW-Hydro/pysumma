import copy


class LocalParamInfo(object):

    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.original_contents = f.readlines()
        self.new_contents = copy.deepcopy(self.original_contents)

    def replace(self, key, default, low=None, uppr=None):
        for i, ln in enumerate(self.new_contents):
            if ln.startswith(key):
                k, de, lo, up = ln.split('|')
                k = k.strip()
                de = de.strip()
                lo = lo.strip()
                up = up.strip()
                if not low:
                    low = lo
                if not uppr:
                    upr = up
                self.new_contents[i] = (ln.replace(de, str(default))
                                          .replace(lo, str(low))
                                          .replace(up, str(upr)))
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
