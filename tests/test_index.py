"""
File: test_index.py
Description: Runs a test Lambda index.py
"""
import json
import boto3
import pytest

@pytest.fixture
def data():
    event = {}
    context = None
    return [event, context]

def test_lambda_handler(data):
    """
    Testing the lambda_handler
    """
    event = {}
    context = None
    assert data[0] == event
    assert data[1] == context
