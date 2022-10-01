from operator import itemgetter

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

for volume in volumes['Volumes']:
    snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [volume['VolumeId']]
            }
        ]
    )

    # sorting the snapshots in descending order based on creation date
    sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

    for snapshot in sorted_by_date[2:]:
        # delete snapshot
        ec2_client.delete_snapshot(
            SnapshotId=snapshot['SnapshotId']
        )

# schedule.every().day.do(delete_old_snapshots)
#
# while True:
#     schedule.run_pending()
