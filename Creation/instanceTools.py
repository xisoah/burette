import time

import boto3
from datetime import datetime
import Data.acdetails as acd
from pprint import pprint
import paramiko
import json
import os


def reqInstance(token, itype, zone, price):
    client = boto3.client('ec2')
    print('Now requesting your instance')
    response = client.request_spot_instances(
        ClientToken=token,  # 'bototestfrankfurt1a3',  # Unique Identifier [boto|dry?|zone|case-no]
        LaunchSpecification={
            'SecurityGroupIds': [acd.getSecGroup(zone)],
            # 'BlockDeviceMappings': [
            #     {
            #         'DeviceName': '/dev/sda1',
            #         # 'VirtualName': 'string',
            #         'Ebs': {
            #             'DeleteOnTermination': False,  # True|False
            #             # 'Iops': 3000,
            #             'SnapshotId': 'snap-073fab32a8710b646',  # snap-0a0c0f8719aa85262
            #             'VolumeSize': 30,
            #             'VolumeType': 'gp2',
            #             # 'KmsKeyId': 'string'
            #         }  # ,
            #         # 'NoDevice': 'string
            #     },
            # ],
            'ImageId': acd.getAMI(zone),  # 'ami-0ac05733838eabc06',
            'InstanceType': itype,
            'KeyName': 'Frankfurt',
            'Monitoring': {
                'Enabled': False
            },
            'Placement': {
                'AvailabilityZone': zone,
            },
            'SubnetId': acd.getSubnet(zone),
        },
        SpotPrice=price,
        Type='persistent',
        InstanceInterruptionBehavior='stop'
    )
    requestID = response['SpotInstanceRequests'][0]['SpotInstanceRequestId']
    return requestID


def reqPteroInstance(token, itype, zone, price):
    client = boto3.client('ec2')
    print('Now requesting your instance')
    response = client.request_spot_instances(
        ClientToken=token,  # 'bototestfrankfurt1a3',  # Unique Identifier [boto|dry?|zone|case-no]
        LaunchSpecification={
            'SecurityGroupIds': [acd.getSecGroup(zone)],
            # 'BlockDeviceMappings': [
            #     {
            #         'DeviceName': '/dev/sda1',
            #         # 'VirtualName': 'string',
            #         'Ebs': {
            #             'DeleteOnTermination': False,  # True|False
            #             # 'Iops': 3000,
            #             'SnapshotId': 'snap-073fab32a8710b646',  # snap-0a0c0f8719aa85262
            #             'VolumeSize': 30,
            #             'VolumeType': 'gp2',
            #             # 'KmsKeyId': 'string'
            #         }  # ,
            #         # 'NoDevice': 'string
            #     },
            # ],
            'ImageId': 'ami-0b9b8579f81c8baa1',  # 'ami-0ac05733838eabc06',
            'InstanceType': itype,
            'KeyName': 'Frankfurt',
            'Monitoring': {
                'Enabled': False
            },
            'Placement': {
                'AvailabilityZone': zone,
            },
            'SubnetId': acd.getSubnet(zone),
        },
        SpotPrice=price,
        Type='persistent',
        InstanceInterruptionBehavior='stop'
    )
    requestID = response['SpotInstanceRequests'][0]['SpotInstanceRequestId']
    return requestID


def getInstance(requestID):
    client = boto3.client('ec2')
    response = client.describe_spot_instance_requests(
        SpotInstanceRequestIds=[requestID]
    )
    instID = response['SpotInstanceRequests'][0]['InstanceId']
    return instID


def readyInst(instID):
    client = boto3.client('ec2')
    response = client.describe_instances(
        InstanceIds=[instID]
    )
    instDict = {
        'PrivateDnsName': response['Reservations'][0]['Instances'][0]['PrivateDnsName'],
        'PrivateIpAddress': response['Reservations'][0]['Instances'][0]['PrivateIpAddress'],
        'PublicDnsName': response['Reservations'][0]['Instances'][0]['PublicDnsName'],
        'PublicIpAddress': response['Reservations'][0]['Instances'][0]['PublicIpAddress'],
        'PublicDnsName': response['Reservations'][0]['Instances'][0]['PublicDnsName'],
    }
    return instDict


def prepareInst(instID):
    print('Now in prepareInst block for ptero in itools')
    instance = defineInstance(instID)
    key = 'D:\\Users\\sohai\\Desktop\\burette\\keys\\' + instance['KeyName'] + '.pub'
    host = str(instance['PublicIpAddress'])
    print(host)  # 35.159.20.213
    sqlHost = repr(host)
    privateIP = instance['PrivateIpAddress']
    print('before ssh')
    ssh = paramiko.SSHClient()
    print('ssh1')
    key = paramiko.RSAKey.from_private_key_file(key)
    print('ssh1')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('ssh1')
    ssh.connect(hostname=host, username='ubuntu', pkey=key)
    commands = ["sudo sed -i 's/18.196.185.249/" + host + "/g' /var/www/pterodactyl/.env",
                "sudo sed -i 's/35.157.82.71/" + host + "/g' /etc/nginx/sites-available/pterodactyl.conf",
                "sudo systemctl restart nginx",
                'mysql -u pterodactyl -h 127.0.0.1 -ppteroburette -D panel -e "UPDATE nodes SET fqdn=' + sqlHost + ', '
                'memory=1024, disk=8192, created_at=now(), updated_at=now() WHERE id=1"',
                "sudo sed -i 's/35.157.82.71/" + host + "/g' /srv/daemon/config/core.json",
                "cd /srv/daemon && sudo npm start",
                "systemctl restart wings"]
    for command in commands:
        print(command)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        if 'npm' in command:
            print('Waiting for 20 seconds npm to run')
            time.sleep(20)


def cancelReq(reqID):
    client = boto3.client('ec2')
    response = client.cancel_spot_instance_requests(
        SpotInstanceRequestIds=[reqID]
    )
    return response


def stopInstance(instID):
    client = boto3.client('ec2')
    response = client.terminate_instances(
        InstanceIds=[instID]
    )
    return response


def defineInstance(instID):
    client = boto3.client('ec2')
    response = client.describe_instances(
        InstanceIds=[instID]
    )
    return response['Reservations'][0]['Instances'][0]


def listInstances(): # Returns data about all instances that exist
    client = boto3.client('ec2')
    response = client.describe_instances(
        MaxResults=500
    )
    activeInstDict = {}
    for instance in response['Reservations']:
        # pprint(instance)
        if not instance['Instances'][0]['State']['Name'] == 'terminated':
            entry = {
                'Type': instance['Instances'][0]['InstanceType'],
                'Zone': instance['Instances'][0]['Placement']['AvailabilityZone'],
                'Key': instance['Instances'][0]['KeyName'],
                'Volume': instance['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId'],
                'IP': instance['Instances'][0]['PublicIpAddress'],
                'SpotID': instance['Instances'][0]['SpotInstanceRequestId'],
                # 'State': instance['Instances'][0]['State']['Name'],
                # 'StateReason': instance['Instances'][0]['StateReason']['Code']
            }
            activeInstDict[instance['Instances'][0]['InstanceId']] = entry
    return activeInstDict


def delVol(instanceID):
    client = boto3.client('ec2')
    response = client.delete_volume(
        VolumeId='string'
    )
    return response


def addtoILedger(instanceID, token):
    filename = '..\\Data\\instanceLedger.json'
    with open(filename, 'r') as f:
        data = json.load(f)
        data[instanceID] = {'Token': token, 'Init': str(datetime.now())}
    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return data


def updateILedger(instanceID, snapshot):
    filename = '..\\Data\\instanceLedger.json'
    with open(filename, 'r') as f:
        data = json.load(f)
        data[instanceID][snapshot] = str(datetime.now())
    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return data


def addtoLedger(instanceID):
    filename = '..\\Data\\ledger.json'
    with open(filename, 'r') as f:
        data = json.load(f)
        client = boto3.client('ec2')
        response = client.describe_instances(
            InstanceIds=[instanceID]
        )

        # data[username] =
        #  Make the ledger here
    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return data


def createSnap():
    client = boto3.client()('ec2')
    response = client.create_snapshots(
        Description='string',
        InstanceSpecification={
            'InstanceId': 'string',
            'ExcludeBootVolume': True | False
        },
        DryRun=True,
        CopyTagsFromSource='volume'
    )


def copySnap():  # Work on this
    client = boto3.client('ec2')
    response = client.copy_snapshot(
        Description='This is my copied snapshot.',
        DestinationRegion='us-east-1',
        SourceRegion='us-west-2',
        SourceSnapshotId='snap-066877671789bd71b',
    )

    print(response)
    response = client.copy_snapshot(
        Description='string',
        Encrypted=True | False,
        KmsKeyId='string',
        SourceRegion='string',
        SourceSnapshotId='string',
        DryRun=True | False
    )
    print(response)
    response = client.copy_image(
        ClientToken='string',
        Description='string',
        Encrypted=True | False,
        KmsKeyId='string',
        Name='string',
        SourceImageId='string',
        SourceRegion='string',
        DryRun=True | False
    )
    print(response)

    # https://github.com/awsdocs/amazon-ec2-user-guide/blob/master/doc_source/ebs-copy-snapshot.md
    # https://docs.aws.amazon.com/cli/latest/reference/ec2/copy-snapshot.html

# To get list of all Images
# client = boto3.client('ec2')
# response = client.describe_images()
# # with open('data.txt', 'w') as outfile:
# #     json.dump(response, outfile)
# for image in response['Images']:
#     if image['ImageId'] == 'ami-0ac05733838eabc06':
#         print(image)
