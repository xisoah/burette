import boto3
from datetime import datetime
import Data.acdetails as acd
from pprint import pprint
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


def getInstance(requestID):
    client = boto3.client('ec2')
    response = client.describe_spot_instance_requests(
        SpotInstanceRequestIds=[requestID]
    )
    instID = response['SpotInstanceRequests'][0]['InstanceId']
    # print(instID)
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
    # print('Please connect to the following link: ' + instDict['PublicDnsName'])
    print('Please use this IP address: ' + instDict['PublicIpAddress'])
    return instDict


def cancelReq(reqID):
    client = boto3.client('ec2')
    response = client.cancel_spot_instance_requests(
        SpotInstanceRequestIds=[reqID]
    )
    return response
# { this is response
#     'CancelledSpotInstanceRequests': [
#         {
#             'SpotInstanceRequestId': 'string',
#             'State': 'active'|'open'|'closed'|'cancelled'|'completed'
#         },
#     ]
# }


def listInstances():
    client = boto3.client('ec2')
    response = client.describe_instances(
        MaxResults=500
    )
    print(response['Reservations'])
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


def copySnap(): # Work on this
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


listInstances()
