AWSTemplateFormatVersion: '2010-09-09'

Resources:
  ENICleanupLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Handler: index.handler
      Role: !GetAtt ENICleanupLambdaRole.Arn
      FunctionName: ENICleanupLambda
      Runtime: python3.8
      Code:
          import boto3
          from datetime import datetime, timedelta
          import json

          def lambda_handler(event, context):
    # Initialize the EC2 client
          ec2 = boto3.client('ec2')

    # Get all ENIs
        response = ec2.describe_network_interfaces()
    
    # Initialize a list to store ENIs to be deleted
        enis_to_delete = []

    # Define the cutoff date (30 days ago)
        cutoff_date = datetime.utcnow() - timedelta(days=30)

    # Iterate through ENIs and identify those that are not attached and older than 30 days
        for eni in response['NetworkInterfaces']:
          if 'Attachment' not in eni or 'AttachmentId' not in eni['Attachment']:
            eni_creation_time = eni['Attachment']['AttachTime']
            if eni_creation_time < cutoff_date:
                enis_to_delete.append(eni['NetworkInterfaceId'])

    # Log or store the information about ENIs to be deleted
      if enis_to_delete:
        print(f"ENIs to be deleted: {enis_to_delete}")
        # You can customize this part to store the information in an S3 bucket, DynamoDB, etc.

    return {
        'statusCode': 200,
        'body': json.dumps('ENI cleanup completed.')
    }

      Timeout: 60

  ENICleanupLambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: ENICleanupLambdaPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - ec2:DescribeNetworkInterfaces
                  - ec2:DeleteNetworkInterface
                Resource: '*'

  ENICleanupEventRule:
    Type: AWS::Events::Rule
    Properties:
      Description: 'Trigger ENI Cleanup Lambda daily'
      ScheduleExpression: 'cron(0 0 * * ? *)'
      State: ENABLED
      Targets:
        - Arn: !GetAtt ENICleanupLambdaFunction.Arn
          Id: ENICleanupLambdaTarget

Outputs:
  LambdaFunctionArn:
    Value: !GetAtt ENICleanupLambdaFunction.Arn
