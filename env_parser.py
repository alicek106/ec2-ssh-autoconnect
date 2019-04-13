import configparser


class EnvParser:
    EC2_SSH_PRIVATE_KEY = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')

        self.EC2_SSH_PRIVATE_KEY = config['CONFIG']['EC2_SSH_PRIVATE_KEY']
