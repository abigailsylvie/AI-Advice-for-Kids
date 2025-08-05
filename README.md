# AI Advice for Kids

This project generates personalized advice for kids using Amazon Bedrock. It helps children learn, grow, and become more obedient based on their age and focus. The advice is saved to S3, and its metadata is stored in DynamoDB.

## Overview

- **Input**: Child’s age and area of focus (e.g. “learning to follow instructions”)
- **Output**: AI-generated advice saved to S3, and metadata stored in DynamoDB
- **Backend**: AWS Lambda function
- **AI Model**: Amazon Bedrock foundation model

---

## How It Works

1. The user provides the child’s age and focus area.
2. The Lambda function sends a prompt to Amazon Bedrock.
3. The generated advice is saved as a `.txt` file in S3.
4. The metadata (age, focus, S3 file path, timestamp) is stored in DynamoDB.

---

## Example Input (Test Event)

```json
{
  "age": 8,
  "focus": "learning to listen to parents and follow instructions"
}
