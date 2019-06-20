from modules.command_processor import CommandProcessor
import logging
import sys

if __name__ == "__main__":
    args = sys.argv
    command = ['connect', 'start', 'stop', 'group', 'list']

    if args[1] not in command:
        logging.error('Invalid arguments.')
        logging.error('Usage: python __main__.py [command: connect or stop] [ec2-instance-name] [options]')
        logging.error('Options :')
        logging.error('--key=mykey (Optional) : Use \'mykey\' as a ssh private key in /etc/ec2_connect_config.ini.')
        logging.error('                         By default, [CONFIG][EC2_SSH_PRIVATE_KEY_DEFAULT] is used.')

        exit(101)

    command_processor = CommandProcessor()
    aws_ec2_manager = command_processor.check_credentials()

    if args[1] == 'connect':
        if len(args) == 4: # It should be fixed later, for more structured parameter way :D
            command_processor.command_connect(aws_ec2_manager, args[2], args[3])
        else:
            command_processor.command_connect(aws_ec2_manager, args[2], None)

    elif args[1] == 'start':
        command_processor.command_start(aws_ec2_manager, args[2])

    elif args[1] == 'stop':
        command_processor.command_stop(aws_ec2_manager, args[2])

    elif args[1] == 'list':
        command_processor.command_list(aws_ec2_manager)

    elif args[1] == 'group':
        if args[2] == 'start':
            command_processor.group_start(aws_ec2_manager, args[3])
        elif args[2] == 'stop':
            command_processor.group_stop(aws_ec2_manager, args[3])

    else:
        logging.error("Argumeht should be 'connect', 'start' or 'stop'")
        exit(101)
