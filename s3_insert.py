import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()


questions_and_answers = {
    "profile_id": "general",
    "Day1": "Alex had a positive and engaging day filled with moments of excitement, \
        creativity, and self-regulation. They enjoyed activities like block stacking, \
            swinging at the park, and painting a rainbow, showcasing determination and \
                enthusiasm. Minor challenges, such as interacting with peers and trying \
                    new foods, were managed with gentle support. Alex effectively used \
                        familiar routines and sensory tools, like their weighted blanket, \
                            to stay calm and focused. The day ended with relaxation after \
                                a story and lullaby, highlighting their adaptability and resilience."
}


# Initialize the S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)

# Specify the bucket name and the key (file name)
bucket_name = 'gptconvodump'
file_key = 'profiles/general_profile.json'  # This can vary based on the profile

try:
    # Convert the dictionary to a JSON string
    json_data = json.dumps(questions_and_answers)
    
    # Upload the JSON data
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=json_data, ContentType='application/json')
    
    print(f"Profile data uploaded to {bucket_name}/{file_key}")
except Exception as e:
    print(f"Error uploading profile data: {e}")
