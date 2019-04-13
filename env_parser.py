import configparser
import os


class EnvParser:
    EC2_SSH_PRIVATE_KEY = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'))

        self.EC2_SSH_PRIVATE_KEY = config['CONFIG']['EC2_SSH_PRIVATE_KEY']
