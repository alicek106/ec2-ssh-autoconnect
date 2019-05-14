from modules import awsutils
import time
import logging


class StatusCode:
    STOPPED = 80
    STOPPING = 64
    RUNNING = 16

class AwsEc2Manager():

    def __init__(self):
        session = awsutils.get_session('ap-northeast-2')
        self.client = session.client('ec2')
        self.client.describe_instances() # Triggers NoCredentialsError Exception

    def __get_instance_data_by_id(self, instance_id):

        """
        Get detailed metadata of EC2 instance.
        :param instance_name: Target EC2 instance to describe metadata.
        :return: Metadata of EC2 instance.
        """

        instance_data = self.client.describe_instances(
            Filters=[
                {'Name': 'instance-id', 'Values': [instance_id]},
            ],
        )
        return instance_data['Reservations'][0]['Instances'][0]

    def __get_instance_data_by_name(self, instance_name):
        instance_data = self.client.describe_instances(
            Filters=[
                {'Name': 'tag:Name', 'Values': [instance_name]}
            ]
        )
        return instance_data['Reservations']

    def start_instances(self, ec2_instance_names):

        """
        Start EC2 instances.
        :param ec2_instance_name: The unique name of EC2 instance to start.
        :return: If already running, return Public IP. If not, return True.
        """

        for ec2_instance_name in ec2_instance_names:
            ec2_instance_data = self.__get_instance_data_by_name(ec2_instance_name)
            # for each Reservations[0], Reservations[1] ... (e.g. instances which have same tag:Name)
            for instances in ec2_instance_data:
                # for each instance when EC2 instances are created at the same time (e.g. by AWS Web UI)
                for instance in instances['Instances']:
                    status = instance['State']['Code']

                    if status == StatusCode.RUNNING:
                        logging.info('EC2 instance is in active.')
                        continue
                        # return ec2_instance_data['PublicIpAddress']

                    # Exception for status 'Terminating', and 'Stopping', etc.
                    elif status != StatusCode.RUNNING and status != StatusCode.STOPPED:
                        logging.error('Instance {} cannot be started. Abort'.format(ec2_instance_name))
                        exit(102)

                    ec2_instance_id = instance['InstanceId']
                    self.client.start_instances(InstanceIds=[ec2_instance_id])
                    logging.info('Starting EC2 instance {} (instance ID : {})...'.format(ec2_instance_name, ec2_instance_id))
        return True

    def check_instance_running(self, ec2_instance_name, max_tries, warmup_time):

        """
        Check whether EC2 instance is running.
        :param ec2_instance_name: EC2 instance name to check health.
        :param max_tries: Seconds to wait until EC2 instance will be active.
        :param warmup_time: Seconds to wait for warm-up when EC2 instance is in active.
        :return: If succeeded to start, return Public IP. If not, return False.
        """

        # For only one instance (For a instance that has unique tag:Name)
        ec2_instance_data = self.__get_instance_data_by_name(ec2_instance_name)
        if len(ec2_instance_data) > 1 or len(ec2_instance_data[0]['Instances']) > 1:
            return -1

        ec2_instance_data = ec2_instance_data[0]['Instances'][0]
        if ec2_instance_data['State']['Code'] == StatusCode.RUNNING:
            logging.info('EC2 instance is in active.')
            return ec2_instance_data['PublicIpAddress']

        for i in range(1, max_tries):
            time.sleep(1)
            ec2_instance_data = self.__get_instance_data_by_name(ec2_instance_name)[0]['Instances'][0]

            if ec2_instance_data['State']['Code'] == StatusCode.RUNNING:
                logging.info('EC2 instance is in active. Waiting for {} seconds for warm-up.'.format(warmup_time))
                time.sleep(warmup_time)
                return ec2_instance_data['PublicIpAddress']

            logging.info('Waiting for starting EC2 instance.. {} tries'.format(i))
        logging.error('Failed to start EC2 instance. Max tries : {}'.format(max_tries))
        return -2

    def stop_instances(self, ec2_instance_names):

        """
        Stop EC2 instance.
        :param ec2_instance_name: Target EC2 instance to stop.
        :return: None
        """
        for ec2_instance_name in ec2_instance_names:
            ec2_instance_data = self.__get_instance_data_by_name(ec2_instance_name)
            # for each Reservations[0], Reservations[1] ... (e.g. instances which have same tag:Name)
            for instances in ec2_instance_data:
                # for each instance when EC2 instances are created at the same time (e.g. by AWS Web UI)
                for instance in instances['Instances']:
                    ec2_instance_id = instance['InstanceId']
                    self.client.stop_instances(InstanceIds=[ec2_instance_id])
                    logging.info('Stopping EC2 instance {} (Instance ID : {})...'.format(ec2_instance_name, ec2_instance_id))

    def check_instance_stopped(self, ec2_instance_name, max_tries):

        """
        Check whether instance is stopped.
        :param ec2_instance_name: Target EC2 instance to check instance is stopped.
        :param max_tries: Seconds to wait until EC2 instance will be stopped.
        :return: If succeeded to stop, return True. If not, return False.
        """

        # For only one instance (For a instance that has unique tag:Name)
        for i in range(1, max_tries):
            time.sleep(1)
            ec2_instance_data = self.__get_instance_data_by_name(ec2_instance_name)[0]['Instances'][0]
            if ec2_instance_data['State']['Code'] == StatusCode.STOPPED:
                return True
            logging.info('Waiting for stopping EC2 instance.. {} tries'.format(i))
        logging.error('Failed to wait stopping EC2 instance. Max tries : {}'.format(max_tries))
        return False

    def print_instance_list(self):
        """
        Print list of EC2 instance including status and IP
        :return: None
        """

        response = self.client.describe_instances()
        name_width = 20 # Default Name label tag width
        instance_list = []
        for instance_group in response['Reservations']:
            for instance in instance_group['Instances']:
                try:
                    name_tag = list(filter(lambda d: d['Key'] == 'Name', instance['Tags']))[0]['Value']
                except KeyError:
                    pass
                name_width = max(name_width, len(name_tag) + 5) # If any instance has long name
                instance_list.append(instance)

        instance_list = sorted(instance_list, key=lambda k: k['State']['Code'])

        print('Instance ID'.ljust(25), 'Instance Name'.ljust(name_width), 'IP Address'.ljust(20), 'Status'.ljust(20), sep='')
        for instance in instance_list:
            instance_id = instance['InstanceId']
            try:
                name_tag = list(filter(lambda d: d['Key'] == 'Name', instance['Tags']))[0]
            except Exception:
                name_tag = {'Value':'<No Name Tag>'}

            instance_data = self.__get_instance_data_by_id(instance_id=instance_id)
            ip_address = instance_data['PublicIpAddress'] if instance_data['State']['Code'] == StatusCode.RUNNING else 'Unknown'
            print(instance_id.ljust(25), name_tag['Value'].ljust(name_width), ip_address.ljust(20),
                  instance_data['State']['Name'].ljust(20), sep='')

