import streamlit as st
import pandas as pd
import os
import boto3
from io import StringIO
from analytics import (
    count_queries,
    extract_keywords,
    average_response_length
)

st.set_page_config(page_title="HealthLiveChat Analytics", layout="wide")
st.title("HealthLiveChat – Admin Analytics Dashboard")

def load_audit_log_from_s3(bucket, key="audit_log.csv"):
    try:
        s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
        obj = s3.get_object(Bucket=bucket, Key=key)
        csv_data = obj['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))
        return df.values.tolist()
    except Exception as e:
        st.error(f"Failed to load audit log from S3: {e}")
        return []

rows = load_audit_log_from_s3(os.getenv("S3_BUCKET"))
if not rows:
    st.warning("No logs found or audit_log.csv is empty.")
    st.stop()

df = pd.DataFrame(rows, columns=["Timestamp", "Query", "Response", "Model", "ImageCaption"])

col1, col2, col3 = st.columns(3)
col1.metric("Total Queries", count_queries(rows))
col2.metric("Avg Response Length (words)", round(average_response_length(rows), 1))
col3.metric("Models Used", df["Model"].nunique())

st.divider()

st.subheader("Most Common Keywords")
keywords = extract_keywords(rows)
st.bar_chart(pd.DataFrame(keywords, columns=["Keyword", "Count"]).set_index("Keyword"))

st.subheader("Raw Log Data")
st.dataframe(df, use_container_width=True, height=300)

st.subheader("Download Logs")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download audit_log.csv", csv, "audit_log.csv", "text/csv")
