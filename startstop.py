import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all instances
    response = ec2.describe_instances()

    start_instances = []
    stop_instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']

            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Action':
                        if tag['Value'] == 'Auto-Start':
                            start_instances.append(instance_id)
                        elif tag['Value'] == 'Auto-Stop':
                            stop_instances.append(instance_id)

    # Start instances
    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print("Started instances:", start_instances)

    # Stop instances
    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        print("Stopped instances:", stop_instances)

    return {
        'statusCode': 200,
        'started': start_instances,
        'stopped': stop_instances
    }
