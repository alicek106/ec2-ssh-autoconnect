import configparser
import unittest
import logging

class EnvParser:
    ENV_BLACK_LIST = ('DEFAULT', 'CONFIG') # Immutable values
    EC2_SSH_PRIVATE_KEY_DEFAULT = None
    EC2_SSH_PRIVATE_KEY_LIST = {}

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('/etc/ec2_connect_config.ini')
        self.EC2_SSH_PRIVATE_KEY_DEFAULT = self.config['CONFIG']['EC2_SSH_PRIVATE_KEY_DEFAULT']
        for key, value in self.config.items('CONFIG'):
            self.EC2_SSH_PRIVATE_KEY_LIST[key] = value

    def get_key_path(self, key_name):
        return self.EC2_SSH_PRIVATE_KEY_LIST[key_name]

    def get_group_list(self, group_name):
        if group_name not in self.config:
            logging.error("Group name {} doesn't exist.".format(group_name))
            return False

        return self.config[group_name]['instance_list'].split()

class EnvParser_test(unittest.TestCase):
    def setUp(self):
        self.env_parser = EnvParser()

    def test_get_group(self):
        group_list = self.env_parser.get_group_list('AWS_KUBE')
        print(group_list)

    def test_read_values(self):
        for value in self.env_parser.config:
            if value not in self.env_parser.ENV_BLACK_LIST:
                print('Section : {}'.format(value))
                print(self.env_parser.config[value]['instance_list'])


if __name__ == '__main__':
    unittest.main()