## Title: Automated EC2 Instance Management Using AWS Lambda


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
<img width="1899" height="946" alt="Screenshot 2026-03-25 202219" src="https://github.com/user-attachments/assets/fc8908f0-a666-415e-b623-2f1b9b6c51a9" />

2. Instance Tags
<img width="1908" height="941" alt="Screenshot 2026-03-25 201744" src="https://github.com/user-attachments/assets/ff36a912-e53e-4969-b565-982a7010ba66" />

<img width="1901" height="954" alt="Screenshot 2026-03-25 201733" src="https://github.com/user-attachments/assets/0feeaf82-53af-4b91-960a-ac959186a068" />


3. Lambda Function Code
<img width="1323" height="486" alt="Screenshot 2026-03-25 202133" src="https://github.com/user-attachments/assets/4cee7b54-0a64-4a85-b4ac-930499e4be1d" />

4. Lambda Test Output
<img width="1899" height="948" alt="Screenshot 2026-03-25 202153" src="https://github.com/user-attachments/assets/829b2609-5599-46cf-ad63-9410a3dae173" />

5. EC2 State Change
<img width="1914" height="946" alt="Screenshot 2026-03-25 203106" src="https://github.com/user-attachments/assets/52647252-033b-48ec-88fc-aaac1e415f47" />

## Tools Used
1. AWS Lambda
2. Amazon EC2
3. IAM
4. Python (Boto3)


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

