import json
import urllib.request
import bs4


# Fetch from github ec2instances.info
def getDict():
    ins_list = []
    ec2infoDict = {}
    test = ''
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
    headers = {'User-Agent': user_agent}
    link = 'https://raw.githubusercontent.com/powdahound/ec2instances.info/master/www/instances.json'
    request = urllib.request.Request(link, None, headers)
    source = urllib.request.urlopen(request).read().decode("utf-8", errors='ignore')
    soup = bs4.BeautifulSoup(source, "html.parser")
    soup = str(soup)
    ec2info_json = json.loads(soup)
    for instance in ec2info_json:
        entry = {
            'ECU': instance['ECU'],
            # 'FPGA': instance['FPGA'],
            'GPU': instance['GPU'],
            'GPU_memory': instance['GPU_memory'],
            'GPU_model': instance['GPU_model'],
            # 'base_performance': instance['base_performance'],
            # 'burst_minutes': instance['burst_minutes'],
            # 'clock_speed_ghz': instance['clock_speed_ghz'],
            # 'compute_capability': instance['compute_capability'],
            # 'ebs_as_nvme': instance['ebs_as_nvme'],
            'ebs_iops': instance['ebs_iops'],
            # 'ebs_max_bandwidth': instance['ebs_max_bandwidth'],
            # 'ebs_optimized': instance['ebs_optimized'],
            # 'ebs_throughput': instance['ebs_throughput'],
            # 'emr': instance['emr'],
            # 'enhanced_networking': instance['enhanced_networking'],
            # 'family': instance['family'],
            # 'generation': instance['generation'],
            # 'intel_avx': instance['intel_avx'],
            # 'intel_avx2': instance['intel_avx2'],
            # 'intel_avx512': instance['intel_avx512'],
            # 'intel_turbo': instance['intel_turbo'],
            # 'memory': instance['memory'],
            # 'physical_processor': instance['physical_processor'],
            'pretty_name': instance['pretty_name']
        }
        ec2infoDict[instance['instance_type']] = entry

    return ec2infoDict
