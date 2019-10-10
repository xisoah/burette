import json
import urllib.request
import bs4
import pandas as pd
import demjson


# Instance details from On-Demand pricing
# instance = 'm5d.4xlarge'
def getDict():
    ins_list = []
    odDict = {}
    links = ['https://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js',
             'https://a0.awsstatic.com/pricing/1/ec2/previous-generation/linux-od.min.js',
             'https://a0.awsstatic.com/pricing/1/deprecated/ec2/linux-od.json']
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
    headers = {'User-Agent': user_agent}
    for link in links:
        request = urllib.request.Request(link, None, headers)
        source = urllib.request.urlopen(request).read().decode("utf-8", errors='ignore')
        soup = bs4.BeautifulSoup(source, "html.parser")
        soup = str(soup)
        if link.endswith('.js'):
            soup = soup.split("(", 1)[1].strip(");")
            ins_json = demjson.decode(soup)
        else:
            ins_json = json.loads(soup)

        # print(py_obj['config']['regions'][0]['instanceTypes'][0]['sizes'][0])  # Use this for debugging
        # print(soup)
        for region in ins_json['config']['regions']:
            # Region is a dictionary
            region_name = region['region']
            ins_loop = len(region['instanceTypes'])
            for indexA in range(ins_loop):
                inst_gen = region['instanceTypes'][indexA]['type']  # Instance Gen
                size_loop = len(region['instanceTypes'][indexA]['sizes'])
                for indexB in range(size_loop):
                    inst_name = region['instanceTypes'][indexA]['sizes'][indexB]['size']  # Instance name
                    inst_vCPU = region['instanceTypes'][indexA]['sizes'][indexB]['vCPU']
                    inst_vECU = region['instanceTypes'][indexA]['sizes'][indexB]['ECU']
                    inst_mem = region['instanceTypes'][indexA]['sizes'][indexB]['memoryGiB']
                    inst_store = region['instanceTypes'][indexA]['sizes'][indexB]['storageGB']
                    entry = [inst_name, inst_vCPU, inst_vECU, inst_mem, inst_store]
                    ins_list.append(entry)
        for entry in ins_list:  # Results from both links are added to dictionary here
            dict_entry = {'vCPU': entry[1], 'vECU': entry[2], 'mem': entry[3], 'store': entry[4]}
            odDict[entry[0]] = dict_entry  # Using the instance type('size') as the key of the dictionary entry

    return odDict
# instanceList = [key for key in ins_dict.keys()]
# # print(instanceList)
# # print(json.dumps(ins_dict, sort_keys=True, indent=4))  # If you need to view dictionary data for debugging
# ins_dt = pd.DataFrame.from_dict(ins_dict, orient='index')
# # print(ins_dt)
# print(ins_dt.loc[instance, :])
