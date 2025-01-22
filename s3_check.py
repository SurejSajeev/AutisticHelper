import boto3
import os
from dotenv import load_dotenv

load_dotenv()
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)

# List all S3 buckets
try:
    response = s3.list_buckets()
    print("Buckets:")
    for bucket in response['Buckets']:
        print(f"Bucket Name: {bucket['Name']}")
        print(f"Creation Date: {bucket['CreationDate']}")
        print("\n")
except Exception as e:
    print(f"Error listing buckets: {e}")
