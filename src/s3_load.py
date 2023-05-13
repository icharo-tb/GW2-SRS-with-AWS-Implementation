import os
from dotenv import load_dotenv

from botocore.config import Config
import boto3

from s3_conn import s3_bucket

def s3_loader(temp,aws_bucket,region,file_name):

    load_dotenv()

    conf = Config(
        region_name = region,
        retries = {
            'max_attempts': 5,
            'mode': 'standard'
        }
    )

    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    
    bucket = s3_bucket(ak=aws_access_key_id,sk=aws_secret_access_key,conf=conf).s3_connector()
    bucket.upload_file(temp,aws_bucket,region,file_name)