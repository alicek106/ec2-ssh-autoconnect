import logging
from modules.env_parser import EnvParser
from modules.aws_ec2_manager import AwsEc2Manager
import botocore
import subprocess


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class CommandProcessor:
    def __init__(self):
        self.env_parser = EnvParser()

    def check_credentials(self):
        try:
            return AwsEc2Manager()
        except botocore.exceptions.ClientError as e:
            logging.error("Invalid credentials")
            exit(103)
        except botocore.exceptions.NoCredentialsError as e:
            logging.error('AWS Credential is not set in environment variable')
            data = self.env_parser.get_ec2_access_key()
            if data == None:
                logging.error("Access key is not specified in config file.")
                exit(102)
            else:
                logging.info("Found access key in config file.")
                return AwsEc2Manager(data)

    def command_connect(self, aws_ec2_manager, arg, key):
        logging.info('Starting EC2 instance : {}'.format(arg))
        aws_ec2_manager.start_instances(ec2_instance_names=[arg])
        public_ip_address = aws_ec2_manager.check_instance_running(ec2_instance_name=arg, max_tries=30, warmup_time=30)
        if public_ip_address is -1:
            logging.error('You are trying to connect the instances which have same tag:Name')
            return

        # private_key = env_parser.EC2_SSH_PRIVATE_KEY if private_key_path is not None else private_key_path
        if key == None:
            cmd = ['ssh', '-oStrictHostKeyChecking=no',
               '-i{}'.format(self.env_parser.EC2_SSH_PRIVATE_KEY_DEFAULT), 'ubuntu@{}'.format(public_ip_address)]
        else:
            key_path = self.env_parser.get_key_path(key.split('=')[1])
            cmd = ['ssh', '-oStrictHostKeyChecking=no',
                   '-i{}'.format(key_path), 'ubuntu@{}'.format(public_ip_address)]
        subprocess.call(cmd)

    def command_start(self, aws_ec2_manager, arg):
        logging.info('Starting EC2 instance : {}'.format(arg))
        aws_ec2_manager.start_instances(ec2_instance_names=[arg])

    def command_stop(self, aws_ec2_manager, arg):
        logging.info('Stopping EC2 instance : {}'.format(arg))
        aws_ec2_manager.stop_instances(ec2_instance_names=[arg])

    def command_list(self, aws_ec2_manager):
        logging.info('List of EC2 instances : ')
        aws_ec2_manager.print_instance_list()

    def group_start(self, aws_ec2_manager, arg):
        group_list = self.env_parser.get_group_list(arg)
        if not group_list:
            return

        aws_ec2_manager.start_instances(group_list)
        for instance_name in group_list:
            aws_ec2_manager.check_instance_running(ec2_instance_name=instance_name, max_tries=30, warmup_time=30)

        logging.info('All instances are ready. You can access the instances using below command \n -> ec2-connect connect [instance name]')

    def group_stop(self, aws_ec2_manager, arg):
        group_list = self.env_parser.get_group_list(arg)
        if not group_list:
            return

        aws_ec2_manager.stop_instances(group_list)