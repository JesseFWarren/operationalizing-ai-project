import boto3
import json

def generate_response_with_bedrock(user_query, context):
    messages = [
        {
            "role": "user",
            "content": f"""
            You are a medical assistant trained on Mayo Clinic data. Use the provided medical context to suggest possible condition, treatment options, 
            and guide the user, but do NOT provide a formal diagnosis. Instead, suggest consulting a healthcare professional. Keep responses to a list of the top 3 likely diseases
            from the provided context. Put spaces/next line inbetween numbers. And before the list introduce that these are the most likely conditions based on reported 
            symptoms. Keep responses concise. 
            Additionally, if the user's symtoms below is just a message without any symptoms listed please ignore the context and reply to the message in a friendly manner.

            Context:
            {context}

            User's Symptoms: {user_query}
            """
        }
    ]

    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

    body = {
        "messages": messages,
        "max_tokens": 400,
        "temperature": 0.7,
        "anthropic_version": "bedrock-2023-05-31"
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId="anthropic.claude-3-haiku-20240307",
        accept="application/json",
        contentType="application/json"
    )

    result = json.loads(response["body"].read())

    return result["content"]
