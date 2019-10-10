import Data.spotPricing as spotPricing
import Data.ec2infoPricing as ec2infoPricing
import Data.odPricing as odPricing
import Data.offerPricing as offerPricing
import Data.manualPricing as manualPricing
import json
import pandas as pd
import sys


def process():
    spotDict = spotPricing.getDict()
    ec2infoDict = ec2infoPricing.getDict()
    odDict = odPricing.getDict()
    offerDict = offerPricing.getDict()
    # manualList = manualPricing.getList()
    # manualDict = dict.fromkeys(manualList)

    for instance in spotDict.keys():
        if instance in ec2infoDict.keys():  # Adding ec2infoDict to spotDict
            spotDict[instance].update(ec2infoDict[instance])
        # odDict and manualDict add nothing new, so we skip them
        # if instance in odDict.keys():  # Adding odDict to spotDict
        #     spotDict[instance].update(odDict[instance])
        if instance in offerDict.keys():  # Adding offerDict to spotDict
            spotDict[instance].update(offerDict[instance])
    return spotDict


# insObj = process()
# # print(json.dumps(dict2, sort_keys=True, indent=4))  # If you need to view dictionary data for debugging
# master_dt = pd.DataFrame.from_dict(insObj, orient='index')
# col = ['pretty_name', 'instanceFamily', 'currentGeneration', 'memory', 'physicalProcessor', 'clockSpeed', 'vCPU',
# 'storage', 'ebs_iops', 'ECU', 'GPU', 'GPU_memory', 'GPU_model', 'processorFeatures', 'networkPerformance',
# 'dedicatedEbsThroughput', 'enhancedNetworking', 'us-east', 'us-east-2', 'us-west-2', 'us-west', 'ca-central-1',
# 'eu-ireland', 'eu-central-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'apac-sin', 'apac-syd', 'apac-tokyo',
# 'ap-northeast-2', 'ap-northeast-3', 'ap-south-1', 'sa-east-1', 'ap-east-1', 'me-south-1']
# master_dt = master_dt[col]
# master_dt.to_excel('df.xlsx')
# print(master_dt)
# print(master_dt.loc[:])
# df = master_dt[['memory', 'eu-central-1', 'eu-ireland']][(master_dt.memory == '4 GiB')]
# df_filtered = master_dt[(master_dt.memory == '4 GiB')]
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(df)
