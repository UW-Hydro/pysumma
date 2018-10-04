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
                k_l, de_l, lo_l, up_l = len(k), len(de), len(lo), len(up)
                if not low:
                    low = lo
                if not uppr:
                    uppr = up
                self.new_contents[i] = (
                    ln.replace(de, str(default).rjust(de_l-1)+' ')
                      .replace(lo, str(low).rjust(lo_l-1)+' ')
                      .replace(up.strip(), str(uppr).strip()))
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
