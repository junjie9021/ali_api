"""
专有网络等接口
https://next.api.aliyun.com/api/Vpc/2016-04-28/CreateVpc?params={}
流程 创建VPC时并创建交换机,交换机绑定VPC
"""
from alibabacloud_vpc20160428 import models
from .client import VPCClient
from pprint import pprint

class VPC(VPCClient):
    """vpc接口"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, region_id, name, **kwargs):
        # cidr_block='192.168.0.0/16' 代表网段
        # 默认3个网段,随机分配 10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
        with self as cli:
            req = models.CreateVpcRequest(region_id=region_id, vpc_name=name, **kwargs)
            res = cli.create_vpc(req)
            return res.to_map() # vpc_id: res['VpcId']

    def delete(self, region_id, vpcid):
        with self as cli:
            req = models.DeleteVpcRequest(region_id=region_id, vpc_id=vpcid,)
            res = cli.delete_vpc(req)
            return res.to_map()

    def get(self, region_id, **kwargs):
        with self as cli:
            req = models.DescribeVpcsRequest(region_id=region_id, **kwargs)
            res = cli.describe_vpcs(req)
            return res.to_map()

    def get_zone_id(self, region_id, **kwargs):
        """查询指定地域中可用区的列表"""
        with self as cli:
            req = models.DescribeZonesRequest(region_id=region_id, **kwargs)
            res = cli.describe_zones(req)
            return res.to_map()


class VSwitch(VPCClient):
    """交换机接口"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, region_id, vpcid, zone_id, name, cidr_block, **kwargs):
        """
        vpcid: vpc_id
        cidr_block: 地址段 10.1.0.0/24
        """
        with self as cli:
            req = models.CreateVSwitchRequest(
                region_id=region_id, 
                zone_id=zone_id, 
                cidr_block=cidr_block, 
                vpc_id=vpcid, **kwargs)
            res = cli.create_vswitch(req)
            return res.to_map() # vs_id: res['VSwitchId']

    def delete(self, region_id, vs_id):
        with self as cli:
            req = models.DeleteVSwitchRequest(region_id=region_id, v_switch_id=vs_id)
            res = cli.delete_vswitch(req)
            return res.to_map()

    def get(self, region_id, vpcid, **kwargs):
        with self as cli:
            req = models.DescribeVSwitchesRequest(region_id=region_id, vpc_id=vpcid, **kwargs)
            res = cli.describe_vswitches(req)
            return res.to_map()['body']

    def get_zone_id(self, region_id, **kwargs):
        """查询指定地域中可用区的列表"""
        with self as cli:
            req = models.DescribeZonesRequest(region_id=region_id, **kwargs)
            res = cli.describe_zones(req)
            return res.to_map()


class NAT(VPCClient):
    """NAT网关接口"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, region_id, vpcid, v_switch_id, name, nat_type='Enhanced', instance_charge_type='PostPaid', **kwargs):
        with self as cli:
            req = models.CreateNatGatewayRequest(
                region_id=region_id, 
                vpc_id=vpcid, 
                name=name,
                v_switch_id=v_switch_id,
                instance_charge_type=instance_charge_type,
                nat_type=nat_type,
                **kwargs)
            res = cli.create_nat_gateway(req)
            return res.to_map() # nat_id: res['NatGatewayId'], forward_table_id: res['ForwardTableIds']['ForwardTableId']

    def delete(self, region_id, natid):
        with self as cli:
            req = models.DeleteNatGatewayRequest(region_id=region_id, nat_gateway_id=natid)
            res = cli.delete_nat_gateway(req)
            return res.to_map()

    def get(self, region_id, **kwargs):
        with self as cli:
            req = models.DescribeNatGatewaysRequest(region_id=region_id, **kwargs)
            res = cli.describe_nat_gateways(req)
            return res.to_map()

    def get_dnat(self, region_id, forward_table_id, **kwargs):
        """查询已创建的DNAT条目,主要用于内网机器端口转发nat网关
        forward_table_id(ForwardTableId): 转发表id
        """
        with self as cli:
            req = models.DescribeForwardTableEntriesRequest(region_id=region_id, forward_table_id=forward_table_id, **kwargs)
            res = cli.describe_forward_table_entries(req)
            return res.to_map()

    def add_dnat(self, region_id, forward_table_id, external_ip, external_port, internal_ip, internal_port, ip_protocol='tcp', **kwargs):
        """在DNAT列表中添加DNAT条目
        external_ip, external_port: 外部ip, 端口
        internal_ip, internal_port: 内部ip, 端口
        forward_entry_name:名称，跟服务器实例名绑定
        """
        with self as cli:
            req = models.CreateForwardEntryRequest(
                        region_id=region_id, 
                        forward_table_id=forward_table_id, 
                        external_ip=external_ip, 
                        external_port=external_port, 
                        internal_ip=internal_ip, 
                        internal_port=internal_port,
                        ip_protocol=ip_protocol,
                        **kwargs)
            res = cli.create_forward_entry(req)
            return res.to_map()

    def remove_dnat(self, region_id, forward_table_id, forward_entry_id):
        """删除指定的DNAT条目
        """
        with self as cli:
            req = models.DeleteForwardEntryRequest(region_id=region_id, forward_table_id=forward_table_id, forward_entry_id=forward_entry_id)
            res = cli.delete_forward_entry(req)
            return res.to_map()

    def update_dnat(self, region_id, forward_table_id, **kwargs):
        with self as cli:
            req = models.ModifyForwardEntryRequest(region_id=region_id, forward_table_id=forward_table_id, **kwargs)
            res = cli.modify_forward_entry(req)
            return res.to_map()


class EIP(VPCClient):
    """EIP弹性ip接口"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, region_id, type='PayByTraffic', bandwidth='200', **kwargs):
        bandwidth = str(bandwidth)
        with self as cli:
            req = models.AllocateEipAddressRequest(region_id=region_id, bandwidth=bandwidth, internet_charge_type=type, **kwargs)
            res = cli.allocate_eip_address(req)
            return res.to_map()

    def delete(self, region_id, eip_id):
        with self as cli:
            req = models.ReleaseEipAddressRequest(region_id=region_id, allocation_id=eip_id)
            res = cli.release_eip_address(req)
            return res.to_map()

    def update(self, region_id, eip_id, bandwidth):
        bandwidth = str(bandwidth)
        with self as cli:
            req = models.ModifyEipAddressAttributeRequest(region_id=region_id, allocation_id=eip_id, bandwidth=bandwidth)
            res = cli.modify_eip_address_attribute(req)
            return res.to_map() 

    def get(self, region_id, **kwargs):
        with self as cli:
            req = models.DescribeEipAddressesRequest(region_id=region_id, **kwargs)
            res = cli.describe_eip_addresses(req)
            return res.to_map()

    def associate(self, region_id, eip_id, in_id, type='Nat'):
        """绑定到实例上,如ECS,NAT"""
        with self as cli:
            req = models.AssociateEipAddressRequest(region_id=region_id, allocation_id=eip_id, instance_id=in_id, instance_type=type)
            res = cli.associate_eip_address(req)
            return res.to_map()

    def unassociate(self, region_id, eip_id, in_id, type='Nat'):
        """解绑,如ECS
        暂时不支持NAT
        """
        with self as cli:
            req = models.UnassociateEipAddressRequest(region_id=region_id, allocation_id=eip_id, instance_id=in_id, instance_type=type)
            res = cli.unassociate_eip_address(req)
            return res.to_map()
