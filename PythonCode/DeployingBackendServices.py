import boto3

# Initialize Boto3 clients for different AWS services
ec2_client = boto3.client('ec2')
autoscaling_client = boto3.client('autoscaling')


# Retrieve information about all VPCs
response = ec2_client.describe_vpcs()

# Find the default VPC
for vpc in response['Vpcs']:
    if vpc['IsDefault']:
        default_vpc_id = vpc['VpcId']
        print(f"Default VPC ID: {default_vpc_id}")
        break

# Define VPC parameters
security_group_name = 'BackendSecurityGroup-Abhi'

# Retrieve subnet information for the default VPC
subnet_response = ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [default_vpc_id]}])

# Get subnet IDs
subnet_ids = [subnet['SubnetId'] for subnet in subnet_response['Subnets']]
print("Subnet IDs:", subnet_ids)


# Retrieve information about all existing security groups
security_groups = ec2_client.describe_security_groups()

security_group_id = None

# Check if the 'SecurityGroup-Abhi' exists
for sg in security_groups['SecurityGroups']:
    if sg['GroupName'] == security_group_name:
        security_group_id = sg['GroupId']
        break

if security_group_id is None:
    # Create a security group for the VPC
    security_group_response = ec2_client.create_security_group(
        Description='Security Group',
        GroupName=security_group_name,
        VpcId=default_vpc_id
    )
    security_group_id = security_group_response['GroupId']

# Define ingress rules for HTTPS, HTTP, and SSH
ip_permissions = [
    {
        'IpProtocol': 'tcp',
        'FromPort': 22,
        'ToPort': 22,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 80,
        'ToPort': 80,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 443,
        'ToPort': 443,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 3001,
        'ToPort': 3001,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 3002,
        'ToPort': 3002,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }
]

# Retrieve the existing IP permissions of the security group
existing_permissions = ec2_client.describe_security_groups(GroupIds=[security_group_id])['SecurityGroups'][0]['IpPermissions']

# Define Auto Scaling Group parameters
launch_configuration_name = 'BackendLaunchConfig-Abhi'
autoscaling_group_name = 'BackendAutoScalingGroup-Abhi'
instance_type = 't2.micro'
desired_capacity = 2
min_size = 1
max_size = 3
subnet_ids_str = ','.join(subnet_ids)


# Check if the launch configuration already exists
response = autoscaling_client.describe_launch_configurations(
    LaunchConfigurationNames=[launch_configuration_name]
)


if 'LaunchConfigurations' in response and response['LaunchConfigurations']:
    # The launch configuration exists, so let's delete it
    existing_launch_config_name = response['LaunchConfigurations'][0]['LaunchConfigurationName']
    print(f"Deleting existing launch configuration: {existing_launch_config_name}")
    
    autoscaling_client.delete_launch_configuration(
        LaunchConfigurationName=existing_launch_config_name
    )

# Check if the launch configuration already exists
response = autoscaling_client.describe_launch_configurations(
    LaunchConfigurationNames=[launch_configuration_name]
)
    
# If the launch configuration doesn't exist, create it
if not response['LaunchConfigurations']:

    user_data_script = """#!/bin/bash
    # Install Docker
    sudo apt update -y
    sudo apt-get install docker.io -y
    sudo service docker start
    sudo usermod -a -G docker ubuntu

    # Pull and run your Docker image
    docker pull public.ecr.aws/c3w1m1q2/abhi-helloservice:3
    docker run -d -p 3001:3001 public.ecr.aws/c3w1m1q2/abhi-helloservice:3
    docker pull public.ecr.aws/c3w1m1q2/abhi-profileservice:21
    docker run -d -p 3002:3002 public.ecr.aws/c3w1m1q2/abhi-profileservice:21
    """


    # Create a launch configuration
    launch_config_response = autoscaling_client.create_launch_configuration(
        LaunchConfigurationName=launch_configuration_name,
        ImageId='ami-03f4878755434977f',
        InstanceType=instance_type,
        SecurityGroups=[security_group_id],
        UserData=user_data_script,
    )

# Check if the Auto Scaling Group exists
response = autoscaling_client.describe_auto_scaling_groups(
    AutoScalingGroupNames=[autoscaling_group_name]
)

if 'AutoScalingGroups' in response and response['AutoScalingGroups']:

    autoscaling_response = autoscaling_client.update_auto_scaling_group(
            AutoScalingGroupName=autoscaling_group_name,
            LaunchConfigurationName=launch_configuration_name,
            MinSize=min_size,
            MaxSize=max_size,
            DesiredCapacity=desired_capacity,
            VPCZoneIdentifier=subnet_ids_str
        )
    print(f"Auto Scaling Group '{autoscaling_group_name}' updated.")
else:
    # Create the Auto Scaling Group
    autoscaling_response = autoscaling_client.create_auto_scaling_group(
        AutoScalingGroupName=autoscaling_group_name,
        LaunchConfigurationName=launch_configuration_name,
        MinSize=min_size,
        MaxSize=max_size,
        DesiredCapacity=desired_capacity,
        VPCZoneIdentifier=subnet_ids_str
    )
