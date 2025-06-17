import csv
import os
import time
from src.retrieval import search
from openai import OpenAI
import boto3

USE_BEDROCK = False
S3_BUCKET = os.getenv("S3_BUCKET")
REGION = os.getenv("AWS_REGION", "us-east-1")
s3 = boto3.client("s3", region_name=REGION)

if USE_BEDROCK:
    from src.bedrock_model import generate_response_with_bedrock as generate_response
    MODEL_SOURCE = "Bedrock"
else:
    from src.chatbot import generate_response_with_openai as generate_response
    MODEL_SOURCE = "OpenAI"

def moderate_input(user_query):
    banned_keywords = ["suicide", "fuck"]
    for word in banned_keywords:
        if word in user_query.lower():
            return False
    return True

def append_to_s3_csv(file_key, row):
    try:
        existing = s3.get_object(Bucket=S3_BUCKET, Key=file_key)["Body"].read().decode("utf-8")
        lines = existing.strip().splitlines()
    except s3.exceptions.NoSuchKey:
        lines = []

    lines.append(",".join(row))
    updated_csv = "\n".join(lines)

    s3.put_object(Bucket=S3_BUCKET, Key=file_key, Body=updated_csv.encode("utf-8"))

def log_interaction(user_query, response, path="chatlog.csv"):
    row = [user_query, response, time.strftime("%Y-%m-%d %H:%M:%S")]

    with open(path, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    append_to_s3_csv("chatlog.csv", row)

def log_audit_entry(user_query, response, path="audit_log.csv"):
    row = [
        time.strftime("%Y-%m-%d %H:%M:%S"),
        user_query,
        response[:100].replace("\n", " "),
        MODEL_SOURCE
    ]

    with open(path, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    append_to_s3_csv("audit_log.csv", row)

def run_pipeline(user_query, retries=3):
    """
    Full chatbot pipeline:
    - Moderate input
    - Retrieve context
    - Generate response via OpenAI or Bedrock
    - Log both interaction and audit entry
    - Retry on failure
    """
    if not moderate_input(user_query):
        return "Your message includes flagged content. Please try again."

    for attempt in range(retries):
        try:
            context = "\n".join(search(user_query)) or "No relevant context found."
            response = generate_response(user_query, context)
            log_interaction(user_query, response)
            log_audit_entry(user_query, response)
            return response
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                return f"Failed after {retries} attempts: {str(e)}"
