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


if __name__ == '__main__':
    unittest.main()