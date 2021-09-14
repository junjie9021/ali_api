from vpc import VPC, NAT, EIP, VSwitch
from ecs import ECS, SecurityGroup, PubKey
from slb import SLB
from pprint import pprint
import time

# 创建一套新环境
# 输入环境名
# 确认云服务器数量，配置
def get_endponit(type, region_id='ap-south-1'):
    # type 产品类型
    api = 'aliyuncs.com'
    types = ['ECS', 'ecs', 'SLB', 'slb', 'VPC', 'vpc']
    if type not in types:
        raise  Exception('type value is not isvalid')
    endpoint = '.'.join([type, region_id, api])
    return endpoint
