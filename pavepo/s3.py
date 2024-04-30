import boto3
from dotenv import load_dotenv
import os
import logging
from botocore.exceptions import ClientError
import io
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

def create_presigned_url(object_name, bucket_name=None, expiration=6000):
    #Создание URL для совместного использования 
    if not bucket_name:
        bucket_name = _AWS_BUCKET_NAME

    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket':bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration,
                                                    )
    except ClientError as e:
        logging.error(e)
        return None

    return response

def upload_object(file_name, bucket=None, object_name=None):
    if not bucket:
        bucket = _AWS_BUCKET_NAME
    # Если S3 object_name не указан, то используется file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Загрузка объекта в облачное хранилище
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return object_name

def save_object(file_path_save, object_name, bucket=None):
    if not bucket:
        bucket = _AWS_BUCKET_NAME
    # Запись объекта из хранилища в файл
    try:
        with open(file_path_save, 'wb') as f:
            s3_client.download_fileobj(bucket, object_name, f)
    except Exception as e:
        logging.error(e)
        return False
    return True

def get_object(object_name, bucket=None):
    if not bucket:
        bucket = _AWS_BUCKET_NAME
    # Получение объекта из хранилища
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=object_name)
    except Exception as e:
        logging.error(e)
        return False
    return obj

if __name__ == "__main__":
    upload_object("C:/Users/alexe/Desktop/pavepo/temp/vid2.mp4")