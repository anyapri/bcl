import boto3
import os
import sys


from src import logger
from src.errors import *


s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

bucket_name = 'bcl-model'

object_key = 'bert_content_processing.mar'

local_file_name = 'app/model_store/bert_content_processing.mar'
logger.info("Started downloading file.")
print("Started downloading file.")
try:
    s3.download_file(bucket_name, object_key, local_file_name)
    logger.info("File downloaded successfully.")
    print("File downloaded successfully.")
except Exception as e:
    msg = f"Error occurred while downloading the file: {e}"
    print(f"Error occurred while downloading the file: {e}.")
    error_500(msg, error_type=ErrorType.S3)

