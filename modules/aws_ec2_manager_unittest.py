import unittest
import warnings
from modules.aws_ec2_manager import AwsEc2Manager

class AwsEc2Manager_test(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.aws_ec2_manager = AwsEc2Manager()

    def test_get_instance_list(self):
        self.aws_ec2_manager.print_instance_list()

    def test_start_instance(self):
        # Alias to avoid long line :D
        awm = self.aws_ec2_manager

        # Start and wait until warm-up
        self.assertTrue(awm.start_instances(ec2_instance_names=['Test']))
        self.assertIsInstance(awm.check_instance_running(ec2_instance_name='Test', max_tries=20, warmup_time=20), str)

        # Start when instance is active
        awm.start_instances(ec2_instance_names=['Test'])

    def test_stop_instance(self):
        # Alias to avoid long line :D
        awm = self.aws_ec2_manager

        # Stop when instance is active
        self.assertIsNone(awm.stop_instances(ec2_instance_names=['Test']))
        self.assertTrue(awm.check_instance_stopped(ec2_instance_name='Test', max_tries=20))

        # Stop when instance is stop
        self.assertIsNone(awm.stop_instances(ec2_instance_names=['Test']))


if __name__ == '__main__':
    unittest.main()