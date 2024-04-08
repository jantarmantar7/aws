echo "Starting the Deployment of Code for Splunk Search App"

# Deployment Region
REGION=ap-south-1

echo "Deploying to $REGION"

# STAGE NAME
STAGE=test  

# CloudFormation STACK NAME
STACK_NAME=${STAGE}-${EnvironmentType}-splunk-search-app 

# ENVIRONMENT TYPE
EnvironmentType=EVAL   

# EC2 key pair
InstanceKeyPair=splunk-instance-key-pair 

 # AMI ID of the EC2 instance
InstanceImageId=ami-09298640a92b2d12c

# HOST ZONE ID of the domain
HostedZoneId=Z0153971118U2PG84DOIP  

#EC2 Instance OS Name
InstanceOS=linux

#Tags
Pod=splunk
Technology=splunk


echo "Deploying to  Stack $STACK_NAME"

sam deploy -t ./cft-1.yaml --capabilities CAPABILITY_NAMED_IAM \
    --stack-name=${STACK_NAME} --region=${REGION} \
    --parameter-overrides  "EnvironmentType=${EnvironmentType}" \
                           "InstanceKeyPair=${InstanceKeyPair}"  \
                           "InstanceImageId=${InstanceImageId}" \
                           "HostedZoneId=${HostedZoneId}" \
                           "Pod=${Pod}" \
                           "Technology=${Technology}"
 