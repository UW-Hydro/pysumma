
# Defines a superclass for any generic key/value pair (key=name, value=value) in a text file
class Option:
    def __init__(self, name, filepath, key_position, value_position, delimiter=None):
        self.name = name
        self.option_filepath = filepath
        self.key_position = key_position
        self.value_position = value_position
        self.delimiter = delimiter
        self.text = self.open_read()
        # Need line_no and line_contents in Option so that write_value can be in Option
        self.line_no = 0
        self.line_contents = ""

    # Opens the file at <filepath> and returns the complete text of the file
    def open_read(self):
        with open(self.option_filepath, 'rt') as f:
            return f.readlines()

    # Opens the file at <filepath> and writes self.text to it (overwrites)
    def edit_save(self):
        with open(self.option_filepath, 'wt') as f:
            f.writelines(self.text)
            f.close()

    # Delimits each line on <delimiter>
    # Picks out the element in <position> in the split-list
    # Returns <line number, line contents> when line_content[position] == name
    def get_line_info(self):
        for line_no, line_contents in enumerate(self.text):
            if line_contents.split(self.delimiter)[self.key_position].startswith(self.name):
                return line_no, line_contents

    # First, gets the complete text from the file at <filepath>
    # Next, replaces the first occurence of <name> <delimiter> <old_value> with <name> <delimiter> <new_value>
    def write_value(self, old_value, new_value):
        self.text = self.open_read() # Read before you write to get the most recent file version
        self.text[self.line_no] = self.line_contents.replace(old_value, new_value, 1)
        self.edit_save()

    # Splits line_contents on <delimiter> (whitespace if none)
    # Returns the split-line list at <position> (String)
    def get_value(self):
        self.line_no, self.line_contents = self.get_line_info()
        words = self.line_contents.split(self.delimiter)
        return words[self.value_position].strip("'")
