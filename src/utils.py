import boto3
from botocore.exceptions import ClientError
import sys, os

from src.config import Config


def get_secret(secret_name: str, region_name="us-east-2") -> str:
    if Config.AWS_ACCESS_KEY == None:
        raise Exception('No AWS_ACCESS_KEY env variable provided')
    if Config.AWS_SECRET_ACCESS_KEY == None:
        raise Exception('No AWS_SECRET_ACCESS_KEY env variable provided')

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
        aws_access_key_id=Config.AWS_ACCESS_KEY,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
    except ClientError as e:
        raise e


def is_running_tests() -> bool:
    if 'pytest' in sys.modules:
        return True
    if 'PYTEST_CURRENT_TEST' in os.environ:
        return True
        
    return False

