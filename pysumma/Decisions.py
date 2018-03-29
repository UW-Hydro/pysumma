from pysumma.Option import Option


class Decisions:
    def __init__(self, filepath):
        self.filepath = filepath
        self.simulStart = SimulDatetime('simulStart', self.filepath)
        self.simulFinsh = SimulDatetime('simulFinsh', self.filepath)
        self.soilCatTbl = DecisionOption('soilCatTbl', self.filepath)
        self.vegeParTbl = DecisionOption('vegeParTbl', self.filepath)
        self.soilStress = DecisionOption('soilStress', self.filepath)
        self.stomResist = DecisionOption('stomResist', self.filepath)
        self.num_method = DecisionOption('num_method', self.filepath)
        self.fDerivMeth = DecisionOption('fDerivMeth', self.filepath)
        self.LAI_method = DecisionOption('LAI_method', self.filepath)
        self.f_Richards = DecisionOption('f_Richards', self.filepath)
        self.groundwatr = DecisionOption('groundwatr', self.filepath)
        self.hc_profile = DecisionOption('hc_profile', self.filepath)
        self.bcUpprTdyn = DecisionOption('bcUpprTdyn', self.filepath)
        self.bcLowrTdyn = DecisionOption('bcLowrTdyn', self.filepath)
        self.bcUpprSoiH = DecisionOption('bcUpprSoiH', self.filepath)
        self.bcLowrSoiH = DecisionOption('bcLowrSoiH', self.filepath)
        self.veg_traits = DecisionOption('veg_traits', self.filepath)
        self.canopyEmis = DecisionOption('canopyEmis', self.filepath)
        self.snowIncept = DecisionOption('snowIncept', self.filepath)
        self.windPrfile = DecisionOption('windPrfile', self.filepath)
        self.astability = DecisionOption('astability', self.filepath)
        self.canopySrad = DecisionOption('canopySrad', self.filepath)
        self.alb_method = DecisionOption('alb_method', self.filepath)
        self.compaction = DecisionOption('compaction', self.filepath)
        self.snowLayers = DecisionOption('snowLayers', self.filepath)
        self.thCondSnow = DecisionOption('thCondSnow', self.filepath)
        self.thCondSoil = DecisionOption('thCondSoil', self.filepath)
        self.spatial_gw = DecisionOption('spatial_gw', self.filepath)
        self.subRouting = DecisionOption('subRouting', self.filepath)


class DecisionOption(Option):
    def __init__(self, name, filepath):
        super().__init__(name, filepath, key_position=0, value_position=1, delimiter=None)
        self.line_no, self.line_contents = self.get_line_info()
        self.get_description()
        self.options = self.get_options()
        self._value = self.get_value()

    def get_description(self):
        num_and_descrip = self.line_contents.split('!')[-1]
        self.description = num_and_descrip.split(')')[-1].strip()
        number = num_and_descrip.find('(')
        self.option_number = num_and_descrip[number+1:number+3]

    def get_options(self):
        start_line = 43
        option_list = []
        for num, line_contents in enumerate(self.text[start_line:]):
            line_num = num + start_line
            if line_contents.startswith('! ({})'.format(self.option_number)):
                while self.text[line_num+1].find("---") < 0 and self.text[line_num+1].find("****") < 0:
                    line_num += 1
                    option_list.append(self.text[line_num].split('!')[1].strip())
                else:
                    return option_list

    @property
    def value(self):
        return self.get_value()

    @value.setter
    def value(self, new_value):
        if new_value in self.options:
            self.write_value(self._value, new_value)
        else:
            raise ValueError('Your input value {} is not one of the valid options {}'.format(new_value, self.options))


class SimulDatetime(DecisionOption):
    def get_default_date_time(self):
        date_time = self.line_contents.split("'")[1]
        return date_time

    @property
    def value(self):
        return self.get_default_date_time()

    @value.setter
    def value(self, new_date_time):
        self.write_value(self._value, new_date_time)
