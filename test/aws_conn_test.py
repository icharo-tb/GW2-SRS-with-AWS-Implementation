"""Boto3

Import Boto3 to test an S3 bucket connection
"""

import boto3
from botocore.config import Config

import dotenv
import os

# Load .env 
dotenv.load_dotenv()

"""Boto3 Config

Base config for boto3 + S3 bucket
"""
conf = Config(
    region_name = 'us-east-1',
    retries = {
        'max_attempts': 5,
        'mode': 'standard'
    }
)

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config = conf
)

"""Main test function

List all s3 buckets
"""
def show_buckets(client):
    
    res = client.list_buckets()

    print('Buckets found:')
    for bucket in res['Buckets']:
        print(f'--> {bucket["Name"]}')

if __name__=='__main__':
    show_buckets(s3)