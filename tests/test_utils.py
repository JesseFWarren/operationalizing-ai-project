import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from src.pipeline import strip_pii, moderate_input
from src.analytics import extract_keywords, average_response_length, count_queries

def test_strip_pii_removes_email():
    text = "Contact me at warrenwjj@gmail.com"
    assert strip_pii(text) == "Contact me at "

def test_strip_pii_removes_credit_card():
    text = "My credit card number is 1234 5678 9012 3456 Please don't use it!"
    assert strip_pii(text) == "My credit card number is  Please don't use it!"

def test_moderate_input_blocks_banned():
    assert not moderate_input("I want to kill myself")

def test_moderate_input_allows_normal():
    assert moderate_input("I have a headache")

def test_extract_keywords_counts_correctly():
    rows = [
        ["2024-01-01", "What is flu?", "response", "OpenAI"],
        ["2024-01-01", "Flu symptoms?", "response", "OpenAI"]
    ]
    keywords = dict(extract_keywords(rows, top_n=2))
    assert "flu" in keywords
    assert keywords["flu"] == 2

def test_average_response_length_words():
    rows = [["2024-01-01", "Q1", "This is four words.", "OpenAI"]]
    avg_len = average_response_length(rows)
    assert avg_len == 4

def test_count_queries():
    rows = [["timestamp", "query", "response", "model", "caption"], ["2024-01-01", "hi", "hello", "gpt", ""]]
    assert count_queries(rows) == 2
