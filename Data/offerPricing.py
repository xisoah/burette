import json
import os
import bs4
from pathlib import Path
from datetime import date, datetime
import urllib.request
import urllib.parse


# Documentation over here https://aws.amazon.com/blogs/aws/new-aws-price-list-api/
# Fetch from Offer file
def getDict():
    current = str(date.today())
    timestamp = os.path.getmtime(Path(__file__).parent / 'offer.json')
    timestamp = datetime.fromtimestamp(timestamp)
    timestamp = timestamp.strftime("%Y-%m-%d")

    # If current = gen, use the offer.json that is already there
    if timestamp == current:
        # To load file from json
        print('offer.json already up-to-date')
        with open(Path(__file__).parent / 'offer.json') as f:
            offer_obj = json.load(f)
        f.close()
        return offer_obj
    else:
        print('Rebuilding offer.json')
        link = 'https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json'
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        headers = {'User-Agent': user_agent}
        request = urllib.request.Request(link, None, headers)
        source = urllib.request.urlopen(request).read().decode("utf-8", errors='ignore')
        soup = bs4.BeautifulSoup(source, "html.parser")
        soup = str(soup)
        offer_data = json.loads(soup)
        offer_obj = {}
        for dct in offer_data['products'].values():
            entry = {
                # 'SKU': dct.get('sku', ''),
                # 'productFamily': dct.get('productFamily', ''),
                # 'serviceCode': dct['attributes'].get('servicecode', ''),
                # 'location': dct['attributes'].get('location', ''),
                # 'locationType':  dct['attributes'].get('locationType', ''),
                'currentGeneration': dct['attributes'].get('currentGeneration', ''),
                'instanceFamily':  dct['attributes'].get('instanceFamily', ''),
                'vCPU': dct['attributes'].get('vcpu', ''),
                'physicalProcessor': dct['attributes'].get('physicalProcessor', ''),
                'clockSpeed': dct['attributes'].get('clockSpeed', ''),
                'memory': dct['attributes'].get('memory', ''),
                'storage':  dct['attributes'].get('storage', ''),
                'networkPerformance': dct['attributes'].get('networkPerformance',   ''),
                # 'processorArchitecture': dct['attributes'].get('processorArchitecture', ''),
                # 'tenancy': dct['attributes'].get('tenancy', ''),
                # 'operatingSystem': dct['attributes'].get('operatingSystem', ''),
                # 'licenseModel': dct['attributes'].get('licenseModel', ''),
                # 'usageType': dct['attributes'].get('usagetype', ''),
                # 'operation': dct['attributes'].get('operation', ''),
                # 'capacityStatus': dct['attributes'].get('capacitystatus', ''),
                'dedicatedEbsThroughput':  dct['attributes'].get('dedicatedEbsThroughput', ''),
                # 'ecu': dct['attributes'].get('ecu', ''),
                'enhancedNetworking': dct['attributes'].get('enhancedNetworkingSupported', ''),
                # 'instanceSKU': dct['attributes'].get('instancesku', ''),
                # 'normalizationSizeFactor': dct['attributes'].get('normalizationSizeFactor', ''),
                # 'preInstalledSw':  dct['attributes'].get('preInstalledSw', ''),
                'processorFeatures': dct['attributes'].get('processorFeatures', '')
            }
            # Do something when instance empty.
            # Dict comprehend this to make it more efficient
            offer_obj[dct['attributes'].get('instanceType', dct['productFamily'])] = entry
        keys = offer_obj.keys()
        # As all instance ids have a '.' in them, we find out weird stuff using following code
        miscOfferKeys = [item for item in keys if '.' not in item]
        # print(sorted(miscOfferKeys))
        miscDict = {key: offer_obj.pop(key) for key in miscOfferKeys}  # Contains weird keys from offer file
        os.remove(Path(__file__).parent / 'offer.json')
        with open(Path(__file__).parent / 'offer.json', 'w') as outfile:
            json.dump(offer_obj, outfile, indent=4)
        return offer_obj


getDict()
# offerObj, miscObj = getDicts()
# pprint.pprint(sorted(offerObj.keys()))
