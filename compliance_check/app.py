import json
import os
import boto3

def get_valid_tags():
    tags = []
    tag_input = os.environ['ListofValidTags']
    tags = tag_input.split('|')
    return tags
    
def get_region_list():
    client = boto3.client('ec2')
    valid_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    return valid_regions
    
def get_instances(AWSregion):
    instances = []
    ec2 = boto3.client('ec2', region_name=AWSregion)
    more_instances = 1
    next_token = 0
    while more_instances > 0:
        print('Requesting ec2 instances')
        if next_token == 0:
            response = ec2.describe_instances()
        else:
            response = ec2.describe_instances(NextToken=next_token)
        print('Processing Payload')
        for reservation in response['Reservations']:
            print('Processing Reservations')
            if 'Instances' in reservation:
                print('Processing Instances')
                for instance in reservation['Instances']:
                    instances.append(instance)
        if 'NextToken' not in response:
            print('No more Instances in Payload')
            more_instances = 0
        else:
            print('More Instances Available')
            next_token = response['NextToken']
    print('{} Total instances returned'.format(len(instances)))
    return instances
            
def record_noncompliance(instance, tag):
    if len(tag) > 1:
        print('Instance {} doesn\'t have any tags'.format(instance['InstanceId']))
    else:
        print('Instance {} doesn\'t have {} tag'.format(instance['InstanceId'], tag))
def process_instances(instances, tags):
    for instance in instances:
        invalid_tag = 0
        if 'Tags' in instance:
            print('Instance {} has tags'.format(instance['InstanceId']))
            for complianceTag in tags:
                print('Checking {} for {} tag'.format(instance['InstanceId'], complianceTag))
                tag_assigned = 0
                for tag in instance['Tags']:
                    if complianceTag == tag['Key']:
                        print('Tag Found!')
                        tag_assigned = 1
                if tag_assigned == 0:
                    record_noncompliance(instance, complianceTag)
                
                        
        else:
            invalid_tag = 1
        if invalid_tag == 1:
            record_noncompliance(instance, tags)
    return True
def lambda_handler(event, context):
    regions = get_region_list()
    tags = get_valid_tags()
    for region in regions:
        print('getting instances form {} region'.format(region))
        instances = get_instances(region)
        process_instances(instances, tags)
        
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": instances,
        }),
    }
