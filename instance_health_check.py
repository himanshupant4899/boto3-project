import boto3
import schedule

ec2_client = boto3.client('ec2')


# instances = ec2_client.describe_instances()

# for reservation in instances['Reservations']:
#     instances = reservation['Instances']
#     for instance in instances:
#         print(instance['State']['Name'])
# The same values van also be obtained through below created code

def check_ec2_status():
    statuses = ec2_client.describe_instance_status(
        IncludeAllInstances=True
    )
    for status in statuses['InstanceStatuses']:
        instance_status = status['InstanceStatus']['Status']
        system_status = status['SystemStatus']['Status']
        state = status['InstanceState']['Name']
        print(f"Instance {status['InstanceId']} status is {instance_status} and system status is {system_status} with state {state}")
    print("#######################################\n")


schedule.every(5).seconds.do(check_ec2_status)

while True:
    schedule.run_pending()
