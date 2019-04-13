import awsutils
import pprint
import time
import logging
import os
import sys
from env_parser import EnvParser
import botocore
import subprocess

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class StatusCode:
    STOPPED = 80
    STOPPING = 64
    RUNNING = 16


class AwsEc2Manager:
    client = None
    ec2_instance_data = None
    ec2_instance_name = None

    def __init__(self, ec2_instance_name):
        session = awsutils.get_session('ap-northeast-2')
        self.client = session.client('ec2')
        self.ec2_instance_name = ec2_instance_name
        self._update_instance_data(ec2_instance_name)

        if self.ec2_instance_data['State']['Code'] != StatusCode.RUNNING and \
                self.ec2_instance_data['State']['Code'] != StatusCode.STOPPED:
            pprint.pprint('Instance is stopping or staring. Try again after few seconds.')
            exit(100)

    def _update_instance_data(self, instance_name):
        instance_data = self.client.describe_instances(
            Filters=[
                {'Name': 'tag:Name', 'Values': [instance_name]}
            ]
        )
        self.ec2_instance_data = instance_data['Reservations'][0]['Instances'][0]

    def start_instance(self):
        # Check whether instance is already running
        if self.ec2_instance_data['State']['Code'] == StatusCode.RUNNING:
            logging.info('EC2 instance is in active.')
            return self.ec2_instance_data['PublicIpAddress']

        # It not running, start and wait
        ec2_instance_id = self.ec2_instance_data['InstanceId']
        self.client.start_instances(InstanceIds=[ec2_instance_id])

        for i in range(1, 30):
            time.sleep(1)
            self._update_instance_data(self.ec2_instance_name)
            if self.ec2_instance_data['State']['Code'] == StatusCode.RUNNING:
                logging.info('EC2 instance is in active. Waiting for 20 seconds for warm-up.')
                time.sleep(20)
                return self.ec2_instance_data['PublicIpAddress']
            logging.info('Waiting for starting EC2 instance.. {} tries'.format(i))
        logging.error('Failed to start EC2 instance. Max tries : 30')
        exit(100)

    def stop_instance(self):
        ec2_instance_id = self.ec2_instance_data['InstanceId']
        self.client.stop_instances(InstanceIds=[ec2_instance_id])


if __name__ == "__main__":
    try:
        flag = sys.argv[1]
    except IndexError as e:
        logging.error("Argument not exist. It can be 'connect' or 'stop'")
        exit(101)

    # Takes configuration from config.ini
    env_parser = EnvParser()
    try:
        awsEc2Manager = AwsEc2Manager(env_parser.AWS_INSTANCE_NAME)
    except botocore.exceptions.NoCredentialsError as e:
        logging.error('AWS Credential is not set in environment variable')
        exit(102)

    if flag == 'connect':
        logging.info('Starting EC2 instance : {}'.format(env_parser.AWS_INSTANCE_NAME))
        public_ip_address = awsEc2Manager.start_instance()
        cmd = ['ssh', '-oStrictHostKeyChecking=no', 
                '-i{}'.format(env_parser.EC2_SSH_PRIVATE_KEY), 'ubuntu@{}'.format(public_ip_address)]
        subprocess.call(cmd)

    elif flag == 'stop':
        logging.info('Stopping EC2 instance : {}'.format(env_parser.AWS_INSTANCE_NAME))
        awsEc2Manager.stop_instance()
    else:
        logging.error("Argumeht should be 'connect' or 'stop'")
        exit(101)
