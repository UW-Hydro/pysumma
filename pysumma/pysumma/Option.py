

'''
    Goal: When instantiated, call get_line_no to store the line_no and line_contents immediately
          This makes the process of getting/setting values easier
          TODO: When writing/changing values, maybe call get_line_no again?

'''


class Option:
    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath
        self.text = self.open_read()
        # Need line_no and line_contents in Option so that write_value can be in Option
        self.line_no = 0
        self.line_contents = ""

    def open_read(self):
        with open(self.filepath, 'rt') as f:
            return f.readlines()

    def edit_save(self):
        with open(self.filepath, 'wt') as f:
            f.writelines(self.text)
    
    # Delimits each line on delimiter
    # Picks out the element in <position> in the split-list
    # Returns <line number, line contents> when line_content[position] == name
    def get_line_info(self, position, delimiter=None):
        for line_no, line_contents in enumerate(self.text):
            if line_contents.split(delimiter)[position].startswith(self.name):
                return line_no, line_contents

    def write_value(self, old_value, new_value):
        self.text[self.line_no] = self.line_contents.replace(old_value, new_value, 1)
        self.edit_save()

    # Splits line_contents on <delimiter> (whitespace if none)
    # Returns the split-line list at <position> (String)
    def get_value(self, position, delimiter=None):
        words = self.line_contents.split(delimiter)
        return words[position]
