import boto3


def get_session(region):
    return boto3.session.Session(region_name=region)