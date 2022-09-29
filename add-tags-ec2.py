import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
instance_ids = []
reservations = ec2_client.describe_instances()['Reservations']

for reservation in reservations:
    instances = reservation['Instances']
    for instance in instances:
        instance_ids.append(instance['InstanceId'])


response = ec2_client.create_tags(
    Resources=instance_ids,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)

