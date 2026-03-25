##Title: Automated EC2 Instance Management Using AWS Lambda


## Objective
To automate the starting and stopping of EC2 instances based on tags using AWS Lambda and Boto3.

---

## Architecture
- AWS Lambda (Python)
- Amazon EC2
- IAM Role
- Boto3 SDK

---

## EC2 Instance Details
Two EC2 instances were created and tagged:

| Instance | Tag Key | Tag Value |
|----------|--------|----------|
| Instance 1 | Action | Auto-Stop |
| Instance 2 | Action | Auto-Start |

---

## IAM Role
- Role Name: LambdaEC2Role
- Policy Attached: AmazonEC2FullAccess

---

## Lambda Function
- Function Name: EC2StartStopFunction
- Runtime: Python 3.x

---

## Steps Followed
Created two EC2 instances
Applied tags (Auto-Start and Auto-Stop)
Created IAM role with EC2 permissions
Developed Lambda function using Python
Implemented tag-based logic
Deployed and tested Lambda function
Verified instance state changes


## Output
Instances with tag Auto-Start → Started
Instances with tag Auto-Stop → Stopped


## Screenshots
1. EC2 Instances List

2. Instance Tags

3. Lambda Function Code

4. Lambda Test Output

5. EC2 State Change

## Tools Used
AWS Lambda
Amazon EC2
IAM
Python (Boto3)


## Code

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

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

    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print("Started instances:", start_instances)

    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        print("Stopped instances:", stop_instances)

    return {
        'statusCode': 200,
        'started': start_instances,
        'stopped': stop_instances
    }

