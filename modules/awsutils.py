import boto3


def get_session(region):
    return boto3.session.Session(region_name=region)

def get_session_with_key(region, data):
    return boto3.session.Session(region_name=region,
                                 aws_access_key_id=data[0],
                                 aws_secret_access_key=data[1])