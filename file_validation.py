"""
Lambda function for validating file content type 
against configured bucket policy.
"""
from urllib.parse import unquote_plus
from html import escape
from magika import Magika
from boto3 import client


m = Magika()

# define which content type is allowed in which bucket
# mime_types from:
# https://github.com/google/magika/blob/main/python/magika/config/content_types_config.json

# upload bucket policy according to your needs
bucket_policy = {
    "my-aws-buckkett": {
        "allowed_content_types": [
            # json
            "application/json",

            # documents
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

            # images
            "image/jpeg",
            "image/png"
        ]
    },
}


def lambda_handler(event, context):
    """
    Lambda handler validates file content type using magika.
    if file content type is not valid then removes file from 
    the bucket.
    """
    # Get the S3 bucket and object key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    obj_key = unquote_plus(event['Records'][0]['s3']['object']['key'])

    print(f'Incoming event for bucket {bucket} object {obj_key}')
    # Initialize S3 client
    s3 = client('s3')

    # validate bucket name so this same
    # function can be used with multiple buckets
    current_bucket_policy = None
    if bucket not in bucket_policy.keys():
        return {
            "error": True,
            "message": "invalid bucket"
        }
    else:
        current_bucket_policy = bucket_policy[bucket]

    # Retrieve the content of the file
    response = s3.get_object(Bucket=bucket, Key=obj_key)
    file_content = response['Body'].read()

    # Perform validation logic here
    is_valid, content_type = validate_file_content(file_content, current_bucket_policy)

    file_name = escape(obj_key.split("/")[-1])
    if is_valid:
        msg = f"File {file_name} has been uploaded with content_type {content_type} to bucket {bucket}"

    else:
        # Reject the upload by deleting object from the bucket
        msg = f"File {file_name} has been rejected with content_type {content_type} to bucket {bucket}"
        s3.delete_object(Bucket=bucket, Key=obj_key)

    print(msg)
    return {
        "error": False,
        "message": msg,
    }


def validate_file_content(content: bytes, s3_bucket_policy: dict):
    """
    validates file content type according to bucket policy.
    returns True if valid else returns False along with 
    file content type
    """
    allowed_content_types = s3_bucket_policy.get("allowed_content_types", None)

    if not allowed_content_types:
        return False, None

    res = m.identify_bytes(content)
    content_type = res.output.mime_type
    if content_type in allowed_content_types:
        return True, content_type

    return False, content_type
