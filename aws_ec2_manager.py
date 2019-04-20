import awsutils
import time
import logging
import unittest
import warnings


class StatusCode:
    STOPPED = 80
    STOPPING = 64
    RUNNING = 16


class AwsEc2Manager_test(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.aws_ec2_manager = AwsEc2Manager()

    def test_start_instance(self):
        # Alias to avoid long line :D
        awm = self.aws_ec2_manager

        # Start and wait until warm-up
        self.assertTrue(awm.start_instance(ec2_instance_name='Test'))
        self.assertIsNot(awm.check_instance_running('Test', max_tries=20, warmup_time=20), False)

        # Start when instance is active
        awm.start_instance(ec2_instance_name='Test')

    def test_stop_instance(self):
        # Alias to avoid long line :D
        awm = self.aws_ec2_manager

        # Stop when instance is active
        self.assertIsNone(awm.stop_instance(ec2_instance_name='Test'))
        self.assertTrue(awm.check_instance_stopped(ec2_instance_name='Test', max_tries=20))

        # Stop when instance is stop
        self.assertIsNone(awm.stop_instance(ec2_instance_name='Test'))


class AwsEc2Manager():

    def __init__(self):
        session = awsutils.get_session('ap-northeast-2')
        self.client = session.client('ec2')
        """
        if self.ec2_instance_data['State']['Code'] != StatusCode.RUNNING and \
                self.ec2_instance_data['State']['Code'] != StatusCode.STOPPED:
            print('Instance is stopping or staring. Try again after few seconds.')
            exit(100)
        """

    def __get_instance_data(self, instance_name):

        """
        Get detailed metadata of EC2 instance.
        :param instance_name: Target EC2 instance to describe metadata.
        :return: Metadata of EC2 instance.
        """

        instance_data = self.client.describe_instances(
            Filters=[
                {'Name': 'tag:Name', 'Values': [instance_name]}
            ]
        )
        return instance_data['Reservations'][0]['Instances'][0]

    def start_instance(self, ec2_instance_name):

        """
        Start EC2 instance.
        :param ec2_instance_name: The unique name of EC2 instance to start.
        :return: If already running, return Public IP. If not, return True.
        """

        ec2_instance_data = self.__get_instance_data(ec2_instance_name)

        if ec2_instance_data['State']['Code'] == StatusCode.RUNNING:
            logging.info('EC2 instance is in active.')
            return ec2_instance_data['PublicIpAddress']

        ec2_instance_id = ec2_instance_data['InstanceId']
        self.client.start_instances(InstanceIds=[ec2_instance_id])
        logging.info('Starting EC2 instance {}...'.format(ec2_instance_name))
        return True

    def check_instance_running(self, ec2_instance_name, max_tries, warmup_time):

        """
        Check whether EC2 instance is running.
        :param ec2_instance_name: EC2 instance name to check health.
        :param max_tries: Seconds to wait until EC2 instance will be active.
        :param warmup_time: Seconds to wait for warm-up when EC2 instance is in active.
        :return: If succeeded to start, return Public IP. If not, return False.
        """

        for i in range(1, max_tries):
            time.sleep(1)
            ec2_instance_data = self.__get_instance_data(ec2_instance_name)

            if ec2_instance_data['State']['Code'] == StatusCode.RUNNING:
                logging.info('EC2 instance is in active. Waiting for {} seconds for warm-up.'.format(warmup_time))
                time.sleep(warmup_time)
                return ec2_instance_data['PublicIpAddress']

            logging.info('Waiting for starting EC2 instance.. {} tries'.format(i))
        logging.error('Failed to start EC2 instance. Max tries : {}'.format(max_tries))
        return False

    def check_instance_stopped(self, ec2_instance_name, max_tries):

        """
        Check whether instance is stopped.
        :param ec2_instance_name: Target EC2 instance to check instance is stopped.
        :param max_tries: Seconds to wait until EC2 instance will be stopped.
        :return: If succeeded to stop, return True. If not, return False.
        """

        for i in range(1, max_tries):
            time.sleep(1)
            ec2_instance_data = self.__get_instance_data(ec2_instance_name)
            if ec2_instance_data['State']['Code'] == StatusCode.STOPPED:
                return True
            logging.info('Waiting for stopping EC2 instance.. {} tries'.format(i))
        logging.error('Failed to wait stopping EC2 instance. Max tries : {}'.format(max_tries))
        return False

    def stop_instance(self, ec2_instance_name):

        """
        Stop EC2 instance.
        :param ec2_instance_name: Target EC2 instance to stop.
        :return: None
        """

        ec2_instance_data = self.__get_instance_data(ec2_instance_name)
        ec2_instance_id = ec2_instance_data['InstanceId']
        self.client.stop_instances(InstanceIds=[ec2_instance_id])
        logging.info('Stopping EC2 instance {}...'.format(ec2_instance_name))


if __name__ == '__main__':
    unittest.main()