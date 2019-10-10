import json
import demjson
import urllib.request
import bs4
import pandas as pd
import numpy as np
instance = 'm5d.4xlarge'


def getDict():
    ins_list = []
    spotDict = {}
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
    headers = {'User-Agent': user_agent}
    link = 'https://spot-price.s3.amazonaws.com/spot.js'
    request = urllib.request.Request(link, None, headers)
    source = urllib.request.urlopen(request).read().decode("utf-8", errors='ignore')
    soup = bs4.BeautifulSoup(source, "html.parser")
    soup = str(soup)
    soup = soup.split("(", 1)[1].strip(");")
    spot_price_json = demjson.decode(soup)
    for region in spot_price_json['config']['regions']:
        # Region is a dictionary
        region_name = region['region']
        ins_loop = len(region['instanceTypes'])
        for indexA in range(ins_loop):
            inst_gen = region['instanceTypes'][indexA]['type']  # Instance Gen
            size_loop = len(region['instanceTypes'][indexA]['sizes'])
            for indexB in range(size_loop):
                inst_name = region['instanceTypes'][indexA]['sizes'][indexB]['size']  # Instance name
                inst_price = region['instanceTypes'][indexA]['sizes'][indexB]['valueColumns'][0]['prices'][
                    'USD']  # Instance price
                entry = [inst_name, inst_gen, region_name, inst_price]
                ins_list.append(entry)
    # for entry in ins_list:
    #     print(entry)
    for entry in ins_list:
        if entry[0] not in spotDict.keys():
            dict_entry = {entry[2]: entry[3]}
            spotDict[entry[0]] = dict_entry
        if entry[0] in spotDict.keys():
            spotDict[entry[0]][entry[2]] = entry[3]

    return spotDict


# instanceList = [key for key in ins_dict.keys()]
# print(instanceList)
# print(json.dumps(ins_dict, sort_keys=True, indent=4)) If you need to view dictionary data for debugging
# ins_df = pd.DataFrame.from_dict(ins_dict, orient='index')  # Instance DataFrame
# # print(ins_df)
# print(ins_df.loc[instance, :])
