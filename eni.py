import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Get current time
    current_time = datetime.now()
    
    # Set the threshold for 30 days
    threshold_time = current_time - timedelta(days=30)
    
    # Describe ENIs
    response = ec2_client.describe_network_interfaces()
    
    # Filter ENIs based on criteria
    filtered_enis = [eni for eni in response['NetworkInterfaces'] if
                     not eni.get('Attachment') and
                     eni.get('Status') == 'available' and
                     eni.get('Attachment') is None and
                     eni.get('CreateTime') <= threshold_time]

    # Print or process the filtered ENIs
    for eni in filtered_enis:
        print(f"Unused ENI found: {eni['NetworkInterfaceId']}")
