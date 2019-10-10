import boto3
import datetime
import Data.master as data


client = boto3.client('ec2', region_name='us-west-2')
regions = [x["RegionName"] for x in client.describe_regions()["Regions"]]

instances = data.process()
for instance in instances:
    # INSTANCE = "c5n.metal"
    print("Instance: %s" % instance)

    results = []

    for region in regions:
        # print(region)
        client = boto3.client('ec2', region_name=region)
        prices = client.describe_spot_price_history(
            InstanceTypes=[instance],
            ProductDescriptions=['Linux/UNIX', 'Linux/UNIX (Amazon VPC)'],
            StartTime=(datetime.datetime.now() -
                       datetime.timedelta(hours=4)).isoformat(),
            MaxResults=1
        )
        # print(prices)
        for price in prices["SpotPriceHistory"]:
            results.append((price["AvailabilityZone"], price["SpotPrice"]))

    for region, price in sorted(results, key=lambda x: x[1]):
        print("Region: %s price: %s" % (region, price))
