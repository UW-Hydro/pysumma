# This class is related with FileManagerOption method in Simulation.py
class Option:
    def __init__(self, name, parent, key_position, value_position, delimiter=None):
        self.name = name
        self.parent = parent
        self.key_position = key_position
        self.value_position = value_position
        self.delimiter = delimiter
        # file_contents is every line of filemanger as list format.
        self.text = parent.file_contents
        # Need line_no and line_contents in Option so that write_value can be in Option
        self.line_no, self.line_contents = self.get_line_info()

    def edit_save(self):
        with open(self.parent.filepath, 'wt') as f:
            f.writelines(self.text)
            f.close()

    # Delimits each line on <delimiter>
    # Picks out the element in <position> in the split-list
    # Returns <line number, line contents> when line_content[position] == name
    def get_line_info(self):
        for line_no, line_contents in enumerate(self.text):
            if line_contents.split(self.delimiter)[self.key_position].strip().startswith(self.name):
                return line_no, line_contents

    def write_value(self, old_value, new_value):
        # self.text = self.open_read() # Read before you write to get the most recent file version
        self.parent.file_contents[self.line_no] = self.line_contents.replace(old_value, new_value, 1)
        self.edit_save()

    # Splits line_contents on <delimiter> (whitespace if none)
    # Returns the split-line list at <position> (String)
    def get_value(self):
        self.line_no, self.line_contents = self.get_line_info()
        words = self.line_contents.split(self.delimiter)
        return words[self.value_position].strip().strip("'")
