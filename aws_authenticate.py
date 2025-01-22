import boto3
import os
# Initialize the STS client
sts_client = boto3.client('sts')

# Function to assume a role
def assume_role(role_arn, session_name):
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name
    )
    
    # Extract temporary credentials
    credentials = response['Credentials']
    print("Temporary Security Credentials:")
    print(f"Access Key ID: {credentials['AccessKeyId']}")
    print(f"Secret Access Key: {credentials['SecretAccessKey']}")
    print(f"Session Token: {credentials['SessionToken']}")
    print(f"Expiration: {credentials['Expiration']}")
    return credentials

# Replace with your Role ARN and Session Name
temp_credentials = assume_role(
    role_arn="arn:aws:iam::831926597648:role/aws-admin",
    session_name="TemporarySession"
)


with open(".env", "w") as env_file:
    env_file.write(f"AWS_ACCESS_KEY_ID={temp_credentials['AccessKeyId']}\n")
    env_file.write(f"AWS_SECRET_ACCESS_KEY={temp_credentials['SecretAccessKey']}\n")
    env_file.write(f"AWS_SESSION_TOKEN={temp_credentials['SessionToken']}\n")
    env_file.write(f"AWS_CREDENTIALS_EXPIRATION={temp_credentials['Expiration'].isoformat()}\n")
