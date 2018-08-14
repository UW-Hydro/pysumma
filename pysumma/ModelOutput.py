import os

class ModelOutput:
    def __init__(self, filepath, master_file_filepath='/var_lookup.f90'):
        self.filepath = filepath
        self.master_file_filepath = os.path.dirname(os.path.abspath('__file__')) + master_file_filepath
        self.text = self.read_file()
        self.var_choices = self.read_master_file()

    # Returns the entire text of the file at self.filepath
    def read_file(self):
        with open(self.filepath, 'rt') as f:
            return f.readlines()

    # Reads var_lookup.f90, the list of all possible ModelOutput variables
    def read_master_file(self):
        out = []
        with open(self.master_file_filepath, 'r') as file:
            for line in file:
                if "::" in line and line.split(sep='::')[1].split(sep='=')[0] is not None:
                    out.append(line.split(sep='::')[1].split(sep='=')[0].strip())
        return out

    # Returns a list of every variable in the file
    def read_variables_from_file(self):
        self.text = self.read_file()
        var_list = []
        for line in self.text:
            if not line.startswith("!"):
                var_list.append(line.split("|")[0].strip())
        return var_list

    # Writes <variable> to ModelOutput.txt iff it's a valid choice AND not already in the file
    def add_variable(self, variable):
        if variable not in self.var_choices:
            raise ValueError("Not a valid variable choice!")
        elif self.check_for_variable(variable) is True:
            raise ValueError("Variable already in file!")
        else:
            with open(self.filepath, 'a') as file:
                file.write(variable + " | 1\n")

    # If <variable> is in the file, return TRUE. Else, return FALSE
    def check_for_variable(self, variable):
        self.text = self.read_file()
        for line in self.text:
            if variable == line.split('|')[0].strip():
                return True
        return False

    # Removes the line ascribed to <variable>
    def remove_variable(self, variable):
        self.text = self.read_file()
        output_text = []
        if variable not in self.var_choices:
            return
        else:
            for line in self.text:
                # If <variable> = the first element on the line (before |)
                if not variable == line.split('|')[0].strip():
                    output_text += line
            # Write the new text (without the line with <variable>) to <filepath>
            with open(self.filepath, 'w') as file:
                file.writelines(output_text)

    # Clears the file of all variables
    def clear_variables(self):
        for var in self.read_variables_from_file():
            self.remove_variable(var)
