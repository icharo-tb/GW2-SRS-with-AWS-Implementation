"""Boto3

Import Boto3 to test an S3 bucket connection
"""

import boto3

class s3_bucket():

    """
    ak = access key
    sk = secret key
    """

    def __init__(self,ak,sk,conf) -> None:
        self.ak = ak
        self.sk = sk
        self.conf = conf

    def s3_connector(self):

        s3 = boto3.client(
            's3',
            aws_access_key_id=self.ak,
            aws_secret_access_key=self.sk,
            config = self.conf
        )

        return s3