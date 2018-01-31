class Decisions:
    def __init__(self, filepath):
        # self.path = path
        # self.filename = filename
        self.filepath = filepath
        self.simulStart = simul_datetime('simulStart', self.filepath)
        self.simulFinsh = simul_datetime('simulFinsh', self.filepath)
        self.soilCatTbl = option('soilCatTbl', self.filepath)
        self.vegeParTbl = option('vegeParTbl', self.filepath)
        self.soilStress = option('soilStress', self.filepath)
        self.stomResist = option('stomResist', self.filepath)
        self.num_method = option('num_method', self.filepath)
        self.fDerivMeth = option('fDerivMeth', self.filepath)
        self.LAI_method = option('LAI_method', self.filepath)
        self.f_Richards = option('f_Richards', self.filepath)
        self.groundwatr = option('groundwatr', self.filepath)
        self.hc_profile = option('hc_profile', self.filepath)
        self.bcUpprTdyn = option('bcUpprTdyn', self.filepath)
        self.bcLowrTdyn = option('bcLowrTdyn', self.filepath)
        self.bcUpprSoiH = option('bcUpprSoiH', self.filepath)
        self.bcLowrSoiH = option('bcLowrSoiH', self.filepath)
        self.veg_traits = option('veg_traits', self.filepath)
        self.canopyEmis = option('canopyEmis', self.filepath)
        self.snowIncept = option('snowIncept', self.filepath)
        self.windPrfile = option('windPrfile', self.filepath)
        self.astability = option('astability', self.filepath)
        self.canopySrad = option('canopySrad', self.filepath)
        self.alb_method = option('alb_method', self.filepath)
        self.compaction = option('compaction', self.filepath)
        self.snowLayers = option('snowLayers', self.filepath)
        self.thCondSnow = option('thCondSnow', self.filepath)
        self.thCondSoil = option('thCondSoil', self.filepath)
        self.spatial_gw = option('spatial_gw', self.filepath)
        self.subRouting = option('subRouting', self.filepath)

class option:
    def __init__(self, name, filepath):
        self.filepath = filepath
        self.open_read()
        self.name = name
        self.get_description()
        self.options = self.get_options()

    def open_read(self):
        with open(self.filepath, 'rt') as f:
            self.text = f.readlines()
        return self.text

    def get_line_no(self, text_startwith):
        text = self.open_read()
        for line_no, line in enumerate(text):
            if line.split()[0].startswith(text_startwith):
                return line_no, line

    def get_default_value(self):
        line_no, line = self.get_line_no(self.name)
        return line.split()[1].strip()

    def get_description(self):
        line_no, line = self.get_line_no(self.name)
        num_and_descrip = line.split('!')[-1]
        self.description = num_and_descrip.split(')')[-1].strip()
        number = num_and_descrip.find('(')
        self.option_number = num_and_descrip[number+1:number+3]

    def get_options(self):
        start_line = 43
        option_list = []
        for num, line in enumerate(self.text[start_line:]):
            line_num = num + start_line
            if line.startswith('! ({})'.format(self.option_number)):
                while self.text[line_num+1].find("---") < 0 and self.text[line_num+1].find("****") < 0:
                    line_num += 1
                    option_list.append(self.text[line_num].split('!')[1].strip())
                else:
                    return option_list

    def wrt_value(self, new_value):
        line_no, line = self.get_line_no(self.name)
        lines = self.open_read()
        lines[line_no] = line.replace(self.value, new_value, 1)
        self.edit_save(lines)

    def edit_save(self, new_lines):
        with open(self.filepath, 'wt') as f:
            f.writelines(new_lines)

    @property
    def value(self):
        return self.get_default_value()

    @value.setter
    def value(self, new_value):
        if new_value in self.options:
            self.wrt_value(new_value)
        else:
            raise ValueError ('Your input value {} is not one of the valid options {}'.format(new_value, self.options))

class simul_datetime(option):
    def get_default_date_time(self):
        line_no, line = self.get_line_no(self.name)
        date_time = line.split("'")[1]
        return date_time

    @property
    def value(self):
        return self.get_default_date_time()

    @value.setter
    def value(self, new_date_time):
        self.wrt_value(new_date_time)

# class file_manager():
#     def __init__(self, path, filename):
#         self.path = path
#         self.filename = filename
#         self.filepath = self.path + self.filename
#         decision_filename = self.open_read()[4].replace("'","/").split("/")[3]
#         return decision_filename
#
#     def open_read(self):
#         with open(self.filepath, 'rt') as f:
#             self.text = f.readlines()
#         return self.text