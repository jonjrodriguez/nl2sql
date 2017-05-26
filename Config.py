from ConfigParser import ConfigParser

class Config(object):
    """
    Config class to read and write options
    """
    def __init__(self, file_name=None):
        self.file_name = file_name or 'config.cfg'

        self.config = ConfigParser()
        self.config.read(['config.example.cfg', self.file_name])


    def set(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)

        self.config.set(section, option, value)


    def remove_option(self, section, option, value):
        if self.config.has_section(section):
            self.config.remove_option(section)

        if len(self.items(section)) == 0:
            self.remove_section(section)


    def remove_section(self, section):
        if self.config.has_section(section):
            self.config.remove_section(section)


    def get(self, section, option, raw=False):
        return self.config.get(section, option, raw)


    def items(self, section):
        return self.config.items(section)


    def has(self, section, option=None):
        if option:
            return self.config.has_option(section, option)

        return self.config.has_section(section)


    def write(self):
        with open(self.file_name, 'wb') as config_file:
            self.config.write(config_file)
