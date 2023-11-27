import logging
from dataclasses import dataclass

import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3_client = boto3.client('s3')


@dataclass
class S3Helper:
    bucket_name: str = "predictus-ocr134811-ocr"

    def download_file(self, object_key):
        try:
            response = s3_client.get_object(Bucket=self.bucket_name, Key=object_key)
            return response['Body'].read()
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error downloading file: {e}")
            raise
