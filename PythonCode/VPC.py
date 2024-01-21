import boto3

# Create a Boto3 EC2 client
ec2_client = boto3.client('ec2')

# Specify the VPC ID for which you want to list subnets
vpc_id = ''

# Describe all subnets in the specified VPC
subnets = ec2_client.describe_subnets(
    Filters=[
        {
            'Name': 'vpc-id',
            'Values': [vpc_id]
        }
    ]
)

# Separate subnets into public and private based on their route table
public_subnets = []
private_subnets = []

for subnet in subnets['Subnets']:
    route_table_associations = subnet.get('Associations', [])
    is_public = any(assoc['Main'] for assoc in route_table_associations)
    
    if is_public:
        public_subnets.append(subnet)
    else:
        private_subnets.append(subnet)

# Print information about public subnets
print("Public Subnets:")
for subnet in public_subnets:
    print(f"Subnet ID: {subnet['SubnetId']}")
    print(f"CIDR Block: {subnet['CidrBlock']}")
    print(f"Availability Zone: {subnet['AvailabilityZone']}")
    print()

# Print information about private subnets
print("Private Subnets:")
for subnet in private_subnets:
    print(f"Subnet ID: {subnet['SubnetId']}")
    print(f"CIDR Block: {subnet['CidrBlock']}")
    print(f"Availability Zone: {subnet['AvailabilityZone']}")
    print()
