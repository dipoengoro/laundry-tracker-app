import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException
import logging
import json
from app.config import settings as env

logger = logging.getLogger(__name__)

s3_client_internal = boto3.client(
    's3',
    endpoint_url=f"http{'s' if env.MINIO_USE_SSL else ''}://{env.MINIO_ENDPOINT}",
    aws_access_key_id=env.MINIO_ACCESS_KEY,
    aws_secret_access_key=env.MINIO_SECRET_KEY,
    config=Config(signature_version='s3v4'),
)

s3_client_public = boto3.client(
    's3',
    endpoint_url=env.MINIO_PUBLIC_ENDPOINT,
    aws_access_key_id=env.MINIO_ACCESS_KEY,
    aws_secret_access_key=env.MINIO_SECRET_KEY,
    config=Config(signature_version='s3v4'),
)

def create_presigned_upload_url(object_name: str, bucket_name: str = env.MINIO_BUCKET, expiration: int = 900) -> str:
    """
    Generates a pre-signed URL for uploading a file to MinIO.
    """
    try:
        response = s3_client_public.generate_presigned_post(
            Bucket=bucket_name,
            Key=object_name,
            ExpiresIn=expiration
        )
        
        # # Replace internal endpoint with public-facing one for the browser
        # internal_endpoint = f"http{'s' if env.MINIO_USE_SSL else ''}://{env.MINIO_ENDPOINT}"
        # public_endpoint = env.MINIO_PUBLIC_ENDPOINT.rstrip('/')
        #
        # if public_endpoint not in response['url']:
        #     response['url'] = response['url'].replace(internal_endpoint, public_endpoint)

        return response
    except ClientError as e:
        logger.error(f"Failed to generate pre-signed upload URL: {e}")
        raise HTTPException(status_code=500, detail="Could not generate upload URL.")

def get_presigned_url(object_name: str, bucket_name: str = env.MINIO_BUCKET, expiration: int = 900) -> str:
    """
    Generates a pre-signed URL to access a file in MinIO.
    """
    try:
        response = s3_client_public.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
        
        # # Replace internal endpoint with public-facing one for the browser
        # internal_endpoint = f"http{'s' if env.MINIO_USE_SSL else ''}://{env.MINIO_ENDPOINT}"
        # public_endpoint = env.MINIO_PUBLIC_ENDPOINT.rstrip('/')
        #
        # if public_endpoint not in response:
        #      response = response.replace(internal_endpoint, public_endpoint)

        return response
    except ClientError as e:
        logger.error(f"Failed to generate pre-signed URL: {e}")
        return None