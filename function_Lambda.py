import boto3
import json
import hashlib
import os
from datetime import datetime

def lambda_handler(event, context):
    # Clients
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
    s3 = boto3.client('s3')
    dynamodb = boto3.client('dynamodb')

    # Environment variables
    BUCKET_NAME = os.environ.get('BUCKET_NAME')
    TABLE_NAME = os.environ.get('TABLE_NAME')
    MODEL_ID = "amazon.nova-pro-v1:0"

    # Step 1: Capture input (default for now)
    age = event.get('age', 8)
    focus = event.get('focus', "being obedient and listening to parents")

    user_message = f"""
    Write advice for a child aged {age} about {focus}.
    Keep it friendly, short,kind,clear, and supportive. 
    Format the response in JSON like this:
    {{
        "title": "Title of the Advice",
        "advice": "The full advice content"
    }}
    """

    request_payload = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": user_message}]
            }
        ],
        "inferenceConfig": {
            "temperature": 0.7,
            "topP": 0.9,
            "maxTokens": 800
        }
    }

    try:
        # Step 2: Call Bedrock
        response = bedrock_runtime.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(request_payload)
        )
        response_body = json.loads(response['body'].read())

        # Step 3: Parse model output
        model_output = response_body.get('output', {}).get('message', {}).get('content', [{}])[0].get('text', '')
        data = json.loads(model_output)

        title = data.get('title', 'Untitled Advice')
        advice_text = data.get('advice', 'No advice provided.')

        # Step 4: Generate UID and timestamp
        uid = hashlib.md5(title.encode()).hexdigest()[:10]
        timestamp = datetime.utcnow().isoformat()

        # Step 5: Save to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"advice/{uid}.txt",
            Body=advice_text
        )

        # Step 6: Save metadata to DynamoDB
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                'uid': {'S': uid},
                'title': {'S': title},
                'age_group': {'S': str(age)},
                'focus_area': {'S': focus},
                'timestamp': {'S': timestamp},
                's3_path': {'S': f"s3://{BUCKET_NAME}/advice/{uid}.txt"}
            }
        )

        # Step 7: Return success
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f"Advice saved successfully!",
                'file': f"advice/{uid}.txt",
                'title': title
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
