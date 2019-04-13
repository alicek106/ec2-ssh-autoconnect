import configparser


class EnvParser:
    AWS_INSTANCE_NAME = None
    EC2_SSH_PRIVATE_KEY = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')

        self.AWS_INSTANCE_NAME = config['CONFIG']['AWS_INSTANCE_NAME']
        self.EC2_SSH_PRIVATE_KEY = config['CONFIG']['EC2_SSH_PRIVATE_KEY']
