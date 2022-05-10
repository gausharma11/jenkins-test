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
    filters = [{'Name': 'instance-state-name', 'Values': ['*']}]
    instances = ec2.instances.filter(Filters=filters)
    all_instances = []
    print("instances==>", instances)

    for instance in instances:
        all_instances.append(instance.id)
        print(instance)
        print(instance.id, instance.type)

    instance_list = json.dumps(all_instances)
    return{"statusCode": 200, "body": instance_list}
