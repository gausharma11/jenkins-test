"""
AWS Python lambda
"""
import json
import boto3

ec2 = boto3.resource('ec2')


def lambda_handler(event, context):
    """ lambda function to list ec2 instances """
    print("event=", event)
    print("context=", context)
    print("test edit")
    filters = [{'Name': 'instance-state-name', 'Values': ['*']}]
    instances = ec2.instances.filter(Filters=filters)
    running_instances = []

    for instance in instances:
        running_instances.append(instance.id)

    instance_list = json.dumps(running_instances)
    return{"statusCode": 200, "body": instance_list}
