from io import StringIO
from components.config import ConfigParser, JsonConfigParser

import unittest

class ConfigParserTests(unittest.TestCase):
    
    def test_parse_config(self):
        with self.assertRaises(NotImplementedError):
            ConfigParser().parse_config(StringIO(""))

class JsonConfigParserTests(unittest.TestCase):
    
    def setUp(self):
        self.expected_json_newbies = """{
    "song": "Lost Stars",
    "artist": "Adam Levine",
    "player": "Spotify"
}"""
        self.config_parser = JsonConfigParser()

    def test_parse_config(self):
        self.assertTrue(len(list(self.config_parser.config_vals.keys())) == 0)
        self.config_parser.parse_config(StringIO(self.expected_json_newbies))
        self.assertTrue(len(list(self.config_parser.config_vals.keys())) == 3)
