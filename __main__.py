from modules.command_processor import CommandProcessor
import logging
import sys

if __name__ == "__main__":
    args = sys.argv
    command = ['connect', 'stop', 'group', 'list']

    if args[1] not in command:
        logging.error('Invalid arguments.')
        logging.error('Usage: python __main__.py [command: connect or stop] [ec2-instance-name]')
        exit(101)

    command_processor = CommandProcessor()
    aws_ec2_manager = command_processor.check_credentials()

    if args[1] == 'connect':
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
        logging.error("Argumeht should be 'connect' or 'stop'")
        exit(101)
