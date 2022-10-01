from operator import itemgetter

import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

# provide the following values
instance_id = ""
availability_zone = ""

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [
                instance_id,
            ]
        },
    ]
)

instance_volume = volumes['Volumes'][0]

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters={
        {
            'Name': 'volume-id',
            'Values': [
                instance_volume['VolumeId'],
            ]
        }
    }
)

latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]

new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone=availability_zone,
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod'
                },
            ]
        },
    ]
)

while True:
    vol = ec2_resource.Volume[new_volume['VolumeId']]
    if vol.state == 'available':
        ec2_resource.Instance(instance_id).attach_volume(
            Device='/dev/xsdb',
            VolumeId=new_volume['VolumeId']
        )
        break
