import json

class ConfigParser(object):
    
    def __init__(self):
        self.config_vals = {}

    def parse_config(self, f):
        """
        Parses the contents of the config file stores it in `config_vals`.
        """
        raise NotImplementedError("I don't know what to do with this file.")

class JsonConfigParser(ConfigParser):
    
    def __init__(self):
        super(JsonConfigParser, self).__init__()

    def parse_config(self, f):
        """
        Obviously, if the JSON file is in the form of a list, this will be no
        good.
        """
        self.config_vals = json.load(f)
