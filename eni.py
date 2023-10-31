import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')

    current_time = datetime.now()
    threshold_time = current_time - timedelta(days=30)

    response = ec2_client.describe_network_interfaces()

    filtered_enis = [eni for eni in response['NetworkInterfaces'] if
                     not eni.get('Attachment') and
                     eni.get('Status') == 'available' and
                     eni.get('Attachment') is None and
                     eni.get('CreateTime') <= threshold_time]

    # Do something with the filtered ENIs (e.g., write to S3, send email, etc.)
    # ...

    return {
        'statusCode': 200,
        'body': 'ENI check completed successfully.'
    }
