import os
import csv
import re
import boto3
from io import StringIO
from pathlib import Path
from collections import Counter

AUDIT_LOG = Path("audit_log.csv")

def load_audit_log(path=AUDIT_LOG):
    bucket = os.getenv("S3_BUCKET")
    key = "audit_log.csv"

    if bucket:
        try:
            s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
            obj = s3.get_object(Bucket=bucket, Key=key)
            csv_data = obj['Body'].read().decode('utf-8')
            reader = csv.reader(StringIO(csv_data))
            return list(reader)
        except Exception as e:
            print(f"Failed to load from S3: {e}")
            return []
    else:
        try:
            with open(path, newline='', encoding='utf-8') as f:
                return list(csv.reader(f))
        except FileNotFoundError:
            print("Local audit_log.csv not found.")
            return []

def count_queries(rows):
    """Count total number of queries"""
    return len(rows)

def extract_keywords(rows, top_n=10):
    """Find most common keywords from user queries"""
    all_words = []
    for row in rows:
        query = row[1]
        words = re.findall(r"\b\w+\b", query.lower())
        all_words.extend(words)
    counter = Counter(all_words)
    return counter.most_common(top_n)

def average_response_length(rows, unit="words"):
    """Compute average length of responses"""
    lengths = []
    for row in rows:
        response = row[2]
        if not isinstance(response, str):
            continue  # Skip rows with invalid response values
        if unit == "words":
            lengths.append(len(response.split()))
        elif unit == "chars":
            lengths.append(len(response))
    return sum(lengths) / len(lengths) if lengths else 0

# testing
if __name__ == "__main__":
    rows = load_audit_log()
    print("Total queries:", count_queries(rows))
    print("Top keywords:", extract_keywords(rows))
    print("Avg response length (words):", average_response_length(rows))
