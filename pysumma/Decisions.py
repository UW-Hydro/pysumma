from pysumma.Option import Option


class Decisions:
    def __init__(self, filepath):
        self.filepath = filepath
        self.file_contents = self.open_read()
        self.simulStart = SimulDatetime(self, 'simulStart')
        self.simulFinsh = SimulDatetime(self, 'simulFinsh')
        self.soilCatTbl = DecisionOption(self, 'soilCatTbl')
        self.vegeParTbl = DecisionOption(self, 'vegeParTbl')
        self.soilStress = DecisionOption(self, 'soilStress')
        self.stomResist = DecisionOption(self, 'stomResist')
        self.num_method = DecisionOption(self, 'num_method')
        self.fDerivMeth = DecisionOption(self, 'fDerivMeth')
        self.LAI_method = DecisionOption(self, 'LAI_method')
        self.f_Richards = DecisionOption(self, 'f_Richards')
        self.groundwatr = DecisionOption(self, 'groundwatr')
        self.hc_profile = DecisionOption(self, 'hc_profile')
        self.bcUpprTdyn = DecisionOption(self, 'bcUpprTdyn')
        self.bcLowrTdyn = DecisionOption(self, 'bcLowrTdyn')
        self.bcUpprSoiH = DecisionOption(self, 'bcUpprSoiH')
        self.bcLowrSoiH = DecisionOption(self, 'bcLowrSoiH')
        self.veg_traits = DecisionOption(self, 'veg_traits')
        self.canopyEmis = DecisionOption(self, 'canopyEmis')
        self.snowIncept = DecisionOption(self, 'snowIncept')
        self.windPrfile = DecisionOption(self, 'windPrfile')
        self.astability = DecisionOption(self, 'astability')
        self.canopySrad = DecisionOption(self, 'canopySrad')
        self.alb_method = DecisionOption(self, 'alb_method')
        self.compaction = DecisionOption(self, 'compaction')
        self.snowLayers = DecisionOption(self, 'snowLayers')
        self.thCondSnow = DecisionOption(self, 'thCondSnow')
        self.thCondSoil = DecisionOption(self, 'thCondSoil')
        self.spatial_gw = DecisionOption(self, 'spatial_gw')
        self.subRouting = DecisionOption(self, 'subRouting')

    def open_read(self):
        with open(self.filepath, 'rt') as f:
            return f.readlines()


class DecisionOption(Option):
    def __init__(self, parent, name):
        super().__init__(name, parent, key_position=0, value_position=1,
                         delimiter=None)

        self.description, self.option_number = self.get_description()
        self.options = self.get_options()
        self._value = self.get_value()

    def get_description(self):
        num_and_descrip = self.line_contents.split('!')[-1]
        description = num_and_descrip.split(')')[-1].strip()
        number = num_and_descrip.find('(')
        option_number = num_and_descrip[number+1:number+3]
        return description, option_number

    def get_options(self):
        start_line = 43
        option_list = []
        for num, line_contents in enumerate(self.parent.file_contents[start_line:]):
            line_num = num + start_line
            if line_contents.startswith('! ({})'.format(self.option_number)):
                while self.parent.file_contents[line_num+1].find("---") < 0 and \
                                self.parent.file_contents[line_num+1].find("****") < 0:
                    line_num += 1
                    option_list.append(self.parent.file_contents[line_num].split('!')[1].strip())
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


class SimulDatetime(Option):
    def __init__(self, parent, name):
        super().__init__(name, parent, key_position=0, value_position=1,
                     delimiter="'")

    @property
    def value(self):
        return self.get_value()

    @value.setter
    def value(self, new_date_time):
        self.write_value(self.value, new_date_time)
