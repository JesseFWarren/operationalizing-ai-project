import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi.testclient import TestClient
from app.main import app
from src.pipeline import run_pipeline
from unittest.mock import patch, mock_open, MagicMock
import pytest
from fastapi import HTTPException

client = TestClient(app)

def test_ask_route():
    res = client.post("/ask", json={"query": "What are flu symptoms?"}, headers={"x-api-key": "secretkey123"})
    assert res.status_code == 200
    assert "response" in res.json()

def test_missing_api_key():
    res = client.post("/ask", json={"query": "hello"})
    assert res.status_code == 401
    assert res.json() == {"detail": "Unauthorized: Invalid or missing API key."}

def test_ask_missing_query():
    res = client.post("/ask", json={}, headers={"x-api-key": "secretkey123"})
    assert res.status_code == 422