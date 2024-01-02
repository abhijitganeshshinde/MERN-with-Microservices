import boto3

# AWS credentials and region
aws_access_key = ''
aws_secret_key = ''
aws_region = 'ap-south-1'

image_id = 'ami-03f4878755434977f'
instance_type = 't3.micro'
key_name = 'abhi'
security_group_ids = ['sg-0f4c2658310168fc7']

user_data_script = """#!/bin/bash
# Install Docker
sudo apt update -y
sudo apt-get install docker.io -y
sudo service docker start
sudo usermod -a -G docker ubuntu

# Pull and run your Docker image
docker pull public.ecr.aws/c3w1m1q2/abhi-feservice:5
docker run -d -p 80:3000 public.ecr.aws/c3w1m1q2/abhi-feservice:5
"""

# Create an EC2 client
ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

# Block device mapping for adjusting root volume size
block_device_mappings = [
    {
        'DeviceName': '/dev/xvda',
        'Ebs': {
            'VolumeSize': 30,  # Set the volume size to 30 GB
            'VolumeType': 'gp2'  # Specify the volume type (e.g., gp2 for General Purpose SSD)
        }
    }
]

# Launch EC2 instances with the specified configuration
response = ec2.run_instances(
    ImageId=image_id,
    InstanceType=instance_type,
    KeyName=key_name,
    SecurityGroupIds=security_group_ids,
    MinCount=1,
    MaxCount=1,
    BlockDeviceMappings=block_device_mappings,
    UserData=user_data_script,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'Frontend-Abhi'
                },
            ]
        }
    ]
)

for instance in response['Instances']:
    print(f"Launched instance {instance['InstanceId']}")
