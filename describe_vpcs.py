import boto3

# region_name to get details from a non default region
ec2_client = boto3.client('ec2')  # ec2_client = boto3.client('ec2', region_name='us-east-1')
available_vpcs = ec2_client.describe_vpcs()
vpcs = available_vpcs['Vpcs']

for vpc in vpcs:
    print(vpc['VpcId'])
    Cidr_Block_Association_Set = vpc['CidrBlockAssociationSet']
    for Association_Set in Cidr_Block_Association_Set:
        print(Association_Set['CidrBlockState'])


ec2_resource = boto3.resource('ec2')
vpc = ec2_resource.create_vpc(
    CidrBlock='10.0.0.0/16'
)
vpc.create_subnet(
    CidrBlock='10.0.1.0/24'
)
vpc.create_subnet(
    CidrBlock='10.0.2.0/24'
)

tags = vpc.create_tags(
    Tags=[
        {
            'Key': 'Name',
            'Value': 'my-vpc'
        },
    ]
)


