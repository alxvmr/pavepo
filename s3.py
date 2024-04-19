import boto3
from dotenv import load_dotenv
import os
import logging
from botocore.exceptions import ClientError
load_dotenv()

_AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
_AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
_AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
_AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

session = boto3.session.Session()
s3_client = session.client(
    service_name = 's3',
    endpoint_url = 'https://hb.vkcs.cloud',
    aws_access_key_id = _AWS_ACCESS_KEY_ID,
    aws_secret_access_key = _AWS_SECRET_ACCESS_KEY,
    region_name = _AWS_DEFAULT_REGION
)

def upload_file(file_name, bucket, object_name=None):
    # Если S3 object_name не указан, то используется file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Загрузка файла в облачное хранилище
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_file(file_path_save, bucket, object_name):
    # Запись файла из хранилища в файл
    try:
        with open(file_path_save, 'wb') as f:
            s3_client.download_fileobj(bucket, object_name, f)
    except Exception as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    upload_file("C:/Users/alexe/Desktop/pavepo/temp/hello.txt", _AWS_BUCKET_NAME)
    get_file("C:/Users/alexe/Desktop/pavepo/temp/hello_output.txt", _AWS_BUCKET_NAME, "hello.txt")
