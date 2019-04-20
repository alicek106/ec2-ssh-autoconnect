import logging
import sys
from env_parser import EnvParser
from aws_ec2_manager import AwsEc2Manager
import botocore
import subprocess


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

env_parser = EnvParser()


def check_credentials():
    try:
        return AwsEc2Manager()
    except botocore.exceptions.NoCredentialsError as e:
        logging.error('AWS Credential is not set in environment variable')
        exit(102)


def command_start(aws_ec2_manager, arg):
    logging.info('Starting EC2 instance : {}'.format(arg))
    aws_ec2_manager.start_instance(ec2_instance_names=[arg])
    public_ip_address = aws_ec2_manager.check_instance_running(ec2_instance_name=arg, max_tries=30, warmup_time=30)

    cmd = ['ssh', '-oStrictHostKeyChecking=no',
       '-i{}'.format(env_parser.EC2_SSH_PRIVATE_KEY), 'ubuntu@{}'.format(public_ip_address)]
    subprocess.call(cmd)


def command_stop(aws_ec2_manager, arg):
    logging.info('Stopping EC2 instance : {}'.format(arg))
    aws_ec2_manager.stop_instance(ec2_instance_names=[arg])


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 3:
        logging.error('Invalid arguments.')
        logging.error('Usage: python __main__.py [command: connect or stop] [ec2-instance-name]')
        exit(101)

    aws_ec2_manager = check_credentials()

    if args[1] == 'connect':
        command_start(aws_ec2_manager, args[2])

    elif args[1] == 'stop':
        command_stop(aws_ec2_manager, args[2])

    elif args[1] == 'group_start':
        # TODO : Implement group start
        print('group start')

    elif args[1] == 'group_stop':
        # TODO : Implement group stop
        print('group stop')

    else:
        logging.error("Argumeht should be 'connect' or 'stop'")
        exit(101)
