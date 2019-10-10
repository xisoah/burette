import json
import boto3
from pkg_resources import resource_filename
from pprint import pprint


# Translate region code to region name
def getAll():
    endpoint_file = resource_filename('botocore', 'data/endpoints.json')
    with open(endpoint_file, 'r') as f:
        data = json.load(f)
        regDict = data['partitions'][0]['regions']
    client = boto3.client('ec2')
    response = client.describe_regions()
    regions = [{region['RegionName']: {'Endpoint': region['Endpoint']}} for region in response['Regions']]
    for region in regions:  # This for loop combines the endpoints with description
        for key, value in region.items():
            regDict[key].update(value)
    for region, value in regDict.copy().items():  # This for loop removes HK and Bah cause we need to opt-in for them.
        if 'Hong Kong' in value['description'] or 'Bahrain' in value['description']:
            del regDict[region]

    for region in regDict.keys():  # Gets zones and subnets
        sublist = []
        client = boto3.client('ec2', region_name=region)
        response = client.describe_subnets()
        a = response['Subnets']
        for item in a:
            entry = {
                    'aZone': item['AvailabilityZone'],
                    'zoneID': item['AvailabilityZoneId'],
                    'ipCount': item['AvailableIpAddressCount'],
                    'cidrBlock': item['CidrBlock'],
                    'state': item['State'],
                    'subnetID': item['SubnetId'],
                    'vpcID': item['VpcId']
                    }
            sublist.append(entry)
        regDict[region]['zones'] = sublist

    for region in regDict.keys():  # Gets security groups
        sglist = []
        client = boto3.client('ec2', region_name=region)
        response = client.describe_security_groups()
        a = response['SecurityGroups']
        for item in a:
            entry = {
                    'groupID': item['GroupId'],
                    'groupName': item['GroupName'],
                    'description': item['Description'],
                    'vpcID': item['VpcId']
                    }
            sglist.append(entry)
        regDict[region]['SecurityGroups'] = sglist
    return regDict
# Write code for fetching the list of keys that I will be assigning later. Cool ya!


def getSecGroup(zone):
    region = zone[:-1]
    sgDict = []
    client = boto3.client('ec2', region_name=region)
    response = client.describe_security_groups()
    a = response['SecurityGroups']
    for item in a:
        # print(item)
        if item['Description'] == 'SSH':
            return item['GroupId']
# getSecGroup('eu-central-1a')


def getSubnet(zone):
    region = zone[:-1]
    client = boto3.client('ec2', region_name=region)
    response = client.describe_subnets()
    a = response['Subnets']
    for item in a:
        if item['AvailabilityZone'] == zone:
            return item['SubnetId']


def getAMI(zone):
    region = zone[:-1]
    amiDict = {
        'eu-central-1': 'ami-0ac05733838eabc06'
    }
    return amiDict[region]

# response = getAll()
# for key, value in response.items():
#     for zone in value['zones']:
#         print(zone['aZone'])
