from pysumma.Option import Option


class Decisions:
    def __init__(self, filepath):
        self.filepath = filepath
        self.simulStart = SimulDatetime('simulStart', self.filepath)
        self.simulFinsh = SimulDatetime('simulFinsh', self.filepath)
        self.soilCatTbl = PDecisionOption('soilCatTbl', self.filepath)
        self.vegeParTbl = PDecisionOption('vegeParTbl', self.filepath)
        self.soilStress = PDecisionOption('soilStress', self.filepath)
        self.stomResist = PDecisionOption('stomResist', self.filepath)
        self.num_method = PDecisionOption('num_method', self.filepath)
        self.fDerivMeth = PDecisionOption('fDerivMeth', self.filepath)
        self.LAI_method = PDecisionOption('LAI_method', self.filepath)
        self.f_Richards = PDecisionOption('f_Richards', self.filepath)
        self.groundwatr = PDecisionOption('groundwatr', self.filepath)
        self.hc_profile = PDecisionOption('hc_profile', self.filepath)
        self.bcUpprTdyn = PDecisionOption('bcUpprTdyn', self.filepath)
        self.bcLowrTdyn = PDecisionOption('bcLowrTdyn', self.filepath)
        self.bcUpprSoiH = PDecisionOption('bcUpprSoiH', self.filepath)
        self.bcLowrSoiH = PDecisionOption('bcLowrSoiH', self.filepath)
        self.veg_traits = PDecisionOption('veg_traits', self.filepath)
        self.canopyEmis = PDecisionOption('canopyEmis', self.filepath)
        self.snowIncept = PDecisionOption('snowIncept', self.filepath)
        self.windPrfile = PDecisionOption('windPrfile', self.filepath)
        self.astability = PDecisionOption('astability', self.filepath)
        self.canopySrad = PDecisionOption('canopySrad', self.filepath)
        self.alb_method = PDecisionOption('alb_method', self.filepath)
        self.compaction = PDecisionOption('compaction', self.filepath)
        self.snowLayers = PDecisionOption('snowLayers', self.filepath)
        self.thCondSnow = PDecisionOption('thCondSnow', self.filepath)
        self.thCondSoil = PDecisionOption('thCondSoil', self.filepath)
        self.spatial_gw = PDecisionOption('spatial_gw', self.filepath)
        self.subRouting = PDecisionOption('subRouting', self.filepath)


class PDecisionOption(Option):
    def __init__(self, name, filepath):
        super().__init__(name, filepath)
        self.line_no, self.line_contents = self.get_line_no_line_contents()
        self.get_description()
        self.options = self.get_options()
        self._value = self.get_default_value()

    # "Overrides" get_line_no_and_contents in Option
    # Puts in the position in the line that will always be the same for any Decision Option
    def get_line_no_line_contents(self):
        return self.get_line_info(0)

    # "Overrides" get_value_of_option in Option
    # Puts in the position in the line that will always be the same for any Decision Option
    def get_default_value(self):
        return self.get_value(1)

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
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value in self.options:
            self.write_value(self._value, new_value)
            self._value = new_value
        else:
            raise ValueError('Your input value {} is not one of the valid options {}'.format(new_value, self.options))


class SimulDatetime(PDecisionOption):
    def get_default_date_time(self):
        date_time = self.line_contents.split("'")[1]
        return date_time

    @property
    def value(self):
        return self.get_default_date_time()

    @value.setter
    def value(self, new_date_time):
        self.write_value(self._value, new_date_time)
