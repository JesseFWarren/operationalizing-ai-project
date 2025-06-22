import csv
import os
import time
from src.retrieval import search
from openai import OpenAI
import boto3
import re
from src.model_api import generate_response, MODEL_SOURCE
from src.vision_model import describe_image

USE_BEDROCK = False
S3_BUCKET = os.getenv("S3_BUCKET")
REGION = os.getenv("AWS_REGION", "us-east-1")
s3 = boto3.client("s3", region_name=REGION)
CACHE = {}

def moderate_input(user_query):
    banned_keywords = [
    "fuck", "shit", "hell", "damn" "suicide", "kill myself", "end my life", "self-harm", "cut myself", "hurt myself",
    "take my life", "overdose", "bleed out", "jump off", "hang myself",
    "harm others", "kill someone", "shoot", "stab", "choke", "murder", "assault", 
    "bomb", "terrorist", "massacre", "school shooting", "arson", "explosive",
    "abuse", "child abuse", "rape", "molest", "sexual assault", "beat", "domestic violence",
    "incest", "harassment", "grooming", "pedophile", "predator",
    "porn", "sex", "sexy", "nude", "nudes", "blowjob", "dick", "vagina", "penis", 
    "fetish", "masturbate", "onlyfans", "stripper",
    "cocaine", "meth", "heroin", "weed", "lsd", "ecstasy", "sell drugs", 
    "buy drugs", "illegal prescription", "fentanyl",
    "racist", "nazi", "white power", "kkk", "hate crime", "bigot", "slur", 
    "homophobic", "transphobic",
    ]
    for word in banned_keywords:
        if word in user_query.lower():
            return False
    return True

def strip_pii(text):
    text = re.sub(r"\b[\w.-]+@[\w.-]+\.\w+\b", "", text)
    text = re.sub(r"\b\d{3}[-.\s]?\d{2,4}[-.\s]?\d{4}\b", "", text)
    text = re.sub(r"\b(?:\d[ -]*?){13,16}\b", "", text)
    return text

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
        "OpenAI"
    ]

    with open(path, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    append_to_s3_csv("audit_log.csv", row)

def run_pipeline(user_query, image_path=None, retries=3):
    """
    Full chatbot pipeline:
    - Moderate input
    - Remove PII
    - Retrieve context
    - Generate response via OpenAI
    - Log interaction and audit
    - Retry on failure
    """
    if not user_query or not isinstance(user_query, str):
        return "Invalid input: Please enter a valid message."

    if not moderate_input(user_query):
        return "Your message includes flagged content. Please try again."

    cleaned_query = strip_pii(user_query)

    # Cache only works for text-only queries
    cache_key = cleaned_query if not image_path else None
    if cache_key and cache_key in CACHE:
        return CACHE[cache_key]

    for attempt in range(retries):
        try:
            image_caption = ""
            if image_path and os.path.exists(image_path):
                image_caption = describe_image(image_path)

            combined_query = f"{image_caption}\n\n{cleaned_query}".strip()
            context = "\n".join(search(combined_query)) or "No relevant context found."
            response = generate_response(combined_query, context)

            log_interaction(combined_query, response)
            log_audit_entry(combined_query, response)

            if cache_key:
               CACHE[cache_key] = response
            return response
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                return f"Failed after {retries} attempts: {str(e)}"