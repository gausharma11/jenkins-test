"""
File: test_index.py
Description: Runs a test Lambda index.py
"""
import json
import boto3

event = {}
context = None

def test_lambda_handler(event, context):
    """
    Testing the lambda_handler
    """
    payload = lambda_handler(event, context)
    assert payload['statusCode'] == 200

if __name__ == '__main__':
    test_lambda_handler(event, context)
