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
```
---
## How to Use
1. Clone the repository

2. Set up an S3 bucket 

3. Create a DynamoDB table  with a partition key 

4. Create a Lambda function and add your code

5. Add the correct IAM role to allow Lambda access to Bedrock, S3, and DynamoDB

6. Test your Lambda function using the sample input JSON
---
## Future Improvements
1. Add a frontend (simple web form) to input age and focus

2. Categorize advice by learning type

3. Send advice by email or SMS
