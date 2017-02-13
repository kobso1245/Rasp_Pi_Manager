from os.path import dirname, join, abspath
import json


class ConfigParser:
    CONFIGURATION = []

    @staticmethod
    def parse_config_file():
        if ConfigParser.CONFIGURATION:
            return ConfigParser.CONFIGURATION[0]
        config_file = join(dirname(dirname(abspath(__file__))),
                           'configuration.json')
        with open(config_file, 'r') as f:
            configuration = json.load(f)
            ConfigParser.CONFIGURATION.append(configuration)
            return configuration
