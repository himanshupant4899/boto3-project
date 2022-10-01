import boto3
import schedule

ec2_client = boto3.client('ec2')
volumes = ec2_client.describe_volumes(
    Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['prod']
            }
        ]
    )


def create_snapshots():
    for volume in volumes['Volumes']:
        snapshot = ec2_client.create_snapshot(
            VolumeId=volume['VolumeId']
        )
        print(snapshot)


schedule.every().day.do(create_snapshots)

while True:
    schedule.run_pending()
