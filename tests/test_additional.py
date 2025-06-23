import os
import pytest
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, mock_open, MagicMock
from io import StringIO

from src.pipeline import append_to_s3_csv, log_interaction, log_audit_entry
from src.pipeline import run_pipeline

os.environ["S3_BUCKET"] = "healthlivechat"
os.environ["AWS_REGION"] = "us-east-2"

@patch("builtins.open", new_callable=mock_open)
@patch("src.pipeline.append_to_s3_csv")
def test_log_interaction(mock_append_s3, mock_file):
    log_interaction("How are you?", "I'm fine.", path="test_log.csv")

    mock_file.assert_called_once_with("test_log.csv", mode="a", newline='', encoding="utf-8")
    mock_append_s3.assert_called_once()
 
@patch("builtins.open", new_callable=mock_open)
@patch("src.pipeline.append_to_s3_csv")
def test_log_audit_entry(mock_append_s3, mock_file):
    log_audit_entry("Headache", "Take some rest.", path="audit_log.csv")

    mock_file.assert_called_once()
    mock_append_s3.assert_called_once()
    assert len(mock_append_s3.call_args[0][1]) == 4 

