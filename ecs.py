from alibabacloud_ecs20140526 import models
from .client import ECSClient
from pprint import pprint


class ECS(ECSClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, region_id, page_size=100, **kwargs) -> list:
        """查询所属地域下的ecs实例详细信息
        接口文档 https://next.api.aliyun.com/api/Ecs/2014-05-26/DescribeInstances?params={}
        返回值参考 https://next.api.aliyun.com/api/Ecs/2014-05-26/DescribeInstances?params={}
        :param region_id:实例所属的地域ID
        """
        with self as cli:
            req = models.DescribeInstancesRequest(region_id=region_id, page_size=page_size, **kwargs)
            res = cli.describe_instances(req).to_map()
            return res['body']

    def get_status(self, region_id, page_size=50, **kwargs) -> list:
        """查询ECS实例的状态信息
        接口文档 https://next.api.alibabacloud.com/api/Ecs/2014-05-26/DescribeInstanceStatus?params={%22RegionId%22:%22ap-south-1%22}&tab=DEMO&lang=PYTHON
        :param region_id:实例所属的地域ID
        """
        with self as cli:
            req = models.DescribeInstanceStatusRequest(region_id=region_id, page_size=page_size, **kwargs)
            res = cli.describe_instance_status(req).to_map()
            return res['body']

    def get_instance_type(self, region_id, image_id, **kwargs) -> list:
        """查询指定镜像支持的实例规格
        接口文档 https://next.api.alibabacloud.com/api/Ecs/2014-05-26/DescribeImageSupportInstanceTypes?params='
        """
        with self as cli:
            req = models.DescribeImageSupportInstanceTypesRequest(region_id=region_id, image_id=image_id, **kwargs)
            res = cli.describe_image_support_instance_types(req)
            return res.to_map()['body']

    def get_images(self, region_id, **kwargs):
        """查询可以使用的镜像资源
        https://next.api.alibabacloud.com/api/Ecs/2014-05-26/DescribeImages?params={}
        """
        with self as cli:
            req = models.DescribeImagesRequest(region_id=region_id, **kwargs)
            res = cli.describe_images(req)
            return res.to_map()['body']


    def create(self, region_id, name, image_id, instance_type, v_switch_id, sg_id, size=40, category='cloud_efficiency', spot_strategy='SpotAsPriceGo', **kwargs):
        """创建实例https://next.api.alibabacloud.com/api/Ecs/2014-05-26/CreateInstance?params={}
        image_id: 镜像id
        instance_type: 实例规格
        v_switch_id: vpc实例id
        磁盘默认 40G，高效磁盘, SpotAsPriceGo抢占式实例
        """
        with self as cli:
            system_disk = models.CreateInstanceRequestSystemDisk(
                    size=size,
                    category=category,
                )
            req = models.CreateInstanceRequest(
                    region_id=region_id,
                    instance_name=name,
                    image_id=image_id,
                    instance_type=instance_type, 
                    v_switch_id=v_switch_id,
                    security_group_id=sg_id,
                    spot_strategy=spot_strategy,
                    system_disk=system_disk,
                    **kwargs)
            res = cli.create_instance(req)
            return res.to_map()['body']

    def delete(self, region_id, in_id, **kwargs):
        """删除实例
        in_id: 实例id;
        in_id为list时,支持批量删除
        """
        with self as cli:
            if isinstance(in_id, str):
                req = models.DeleteInstanceRequest(instance_id=in_id, **kwargs)
                res = cli.delete_instance(req)
            if isinstance(in_id, list):
                req = models.DeleteInstancesRequest(region_id=region_id, instance_id=in_id, **kwargs)
                res = cli.delete_instances(req)
            return res.to_map()['body']

    def update(self):
        pass

    def options_ecs(self, option, region_id, in_id, batch_optimization='SuccessFirst', **kwargs):
        """实例操作, 启动, 停止, 重启
        """
        with self as cli:
            if isinstance(in_id, str):
                if option == 'start':
                    req = models.StartInstanceRequest(instance_id=in_id, **kwargs)
                    res = cli.start_instance(req)
                if option == 'stop':
                    req = models.StopInstanceRequest(instance_id=in_id, **kwargs)
                    res = cli.stop_instance(req)
                if option == 'restart':
                    req = models.RebootInstanceRequest(instance_id=in_id, **kwargs)
                    res = cli.reboot_instance(req)
            if isinstance(in_id, list):
                if option == 'start':
                    req = models.StartInstancesRequest(region_id=region_id, instance_id=in_id, batch_optimization=batch_optimization, **kwargs)
                    res = cli.start_instances(req)
                if option == 'stop':
                    req = models.StopInstancesRequest(region_id=region_id, instance_id=in_id, batch_optimization=batch_optimization, **kwargs)
                    res = cli.stop_instances(req)
                if option == 'restart':
                    req = models.RebootInstancesRequest(region_id=region_id, instance_id=in_id, batch_optimization=batch_optimization, **kwargs)
                    res = cli.reboot_instances(req)
            return res.to_map()['body']

    def start(self, region_id, in_id, batch_optimization='SuccessFirst', **kwargs):
        return self.options_ecs('start', region_id, in_id, batch_optimization='SuccessFirst', **kwargs)

    def stop(self, region_id, in_id, batch_optimization='SuccessFirst', **kwargs):
        return self.options_ecs('stop',  region_id, in_id, batch_optimization='SuccessFirst', **kwargs)

    def restart(self, region_id, in_id, batch_optimization='SuccessFirst', **kwargs):
        return self.options_ecs('restart',  region_id, in_id, batch_optimization='SuccessFirst', **kwargs)

class PubKey(ECSClient):
    """
    密钥对 api
    接口文档 https://next.api.alibabacloud.com/api/Ecs/2014-05-26/CreateKeyPair?params={}
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, region_id, key_name, **kwargs):
        """新建
        """
        with self as cli:
            req = models.CreateKeyPairRequest(region_id=region_id, key_pair_name=key_name, **kwargs)
            res = cli.create_key_pair(req)
            return res.to_map()['body']

    def delete(self, region_id, key_name):
        """删除"""
        if isinstance(key_name, str):
            key_name = str([key_name])
        if isinstance(key_name, list):
            key_name = str(key_name)
        with self as cli:
            req = models.DeleteKeyPairsRequest(region_id=region_id, key_pair_names=key_name)
            res = cli.delete_key_pairs(req)
            return res.to_map()['body']

    def get(self, region_id, **kwargs):
        with self as cli:
            req = models.DescribeKeyPairsRequest(region_id=region_id, **kwargs)
            res = cli.describe_key_pairs(req)
            return res.to_map()['body']

class SecurityGroup(ECSClient):
    """
    安全组api接口
    接口文档https://next.api.alibabacloud.com/api/Ecs/2014-05-26/CreateSecurityGroup?params={}
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def create(self, region_id, vpcid, sg_name, **kwargs):
        """新建安全组
        """
        with self as cli:
            req = models.CreateSecurityGroupRequest(region_id=region_id, security_group_name=sg_name, vpc_id=vpcid, **kwargs)
            res = cli.create_security_group(req)
            return res.to_map()['body']

    def delete(self, region_id, sg_id):
        """删除安全组
        """
        with self as cli:
            req = models.DeleteSecurityGroupRequest(region_id=region_id, security_group_id=sg_id)
            res = cli.delete_security_group(req)
            return res.to_map()['body']

    def get(self, region_id, **kwargs) -> list:
        """获取安全组
        """
        with self as cli:
            req = models.DescribeSecurityGroupsRequest(region_id=region_id, **kwargs)
            res = cli.describe_security_groups(req)
            return res.to_map()['body']

    def add(self, sg_id, in_id):
        """将实例添加进安全组
        :param sg_id: 安全组id
        :param in_id: 实例id
        """
        with self as cli:
            req = models.JoinSecurityGroupRequest(security_group_id=sg_id, instance_id=in_id)
            res = cli.join_security_group(req)
            return res.to_map()['body']

    def remove(self, sg_id, in_id):
        """将实例移出安全组
        """
        with self as cli:
            req = models.LeaveSecurityGroupRequest(security_group_id=sg_id, instance_id=in_id)
            res = cli.leave_security_group(req)
            return res.to_map()['body']

    types = ['tcp', 'udp', 'icmp', 'gre', 'all']
    def open_port(self, region_id, sg_id, type, port, source_cidr_ip='0.0.0.0/0', **kwargs):
        """增加一条入方向组规则,开放端口
        type: 协议['tcp', 'udp', 'icmp', 'gre', 'all']
        """
        if type not in self.types:
            raise Exception('type param error')
        # port 处理下格式,如设置8080,格式后为 8080/8080
        if isinstance(port, int):
            port = str(port) + '/' + str(port)
        if isinstance(port, str):
            if '/' not in port:
                port = port + '/' + port
        with self as cli:
            req = models.AuthorizeSecurityGroupRequest(
                        region_id=region_id,
                        security_group_id=sg_id, 
                        ip_protocol=type, 
                        port_range=port,
                        source_port_range=port,
                        source_cidr_ip=source_cidr_ip,
                        **kwargs)
            res = cli.authorize_security_group(req)
            return res.to_map()['body']

    def close_port(self, region_id, sg_id, type, port, source_cidr_ip='0.0.0.0/0', **kwargs):
        """删除入方向的组规则,关闭端口
        """
        if type not in self.types:
            raise Exception('type param error')
        # port 处理下格式,如设置8080,格式后为 8080/8080
        if isinstance(port, int):
            port = str(port) + '/' + str(port)
        if isinstance(port, str):
            if '/' not in port:
                port = port + '/' + port
        with self as cli:
            req = models.RevokeSecurityGroupRequest(
                        region_id=region_id,
                        security_group_id=sg_id, 
                        ip_protocol=type, 
                        port_range=port,
                        source_port_range=port,
                        source_cidr_ip=source_cidr_ip,
                        **kwargs)
            res = cli.revoke_security_group(req)
            return res.to_map()['body']

    def get_ports(self, region_id, sg_id, **kwargs):
        """获取安全组规则
        """
        with self as cli:
            req = models.DescribeSecurityGroupAttributeRequest(region_id=region_id, security_group_id=sg_id)
            res = cli.describe_security_group_attribute(req)
            return res.to_map()['body']


class Image(ECSClient):
    """镜像操作
    doc: https://next.api.aliyun.com/api/Ecs/2014-05-26/DescribeImages?params={}
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def get(self, region_id, **kwargs):
        with self as cli:
            req = models.DescribeImagesRequest(region_id=region_id, **kwargs)
            res = cli.describe_images(req)
            return res.to_map()['body']

    def create(self, region_id, in_id, name, **kwargs):
        with self as cli:
            req = models.CreateImageRequest(region_id=region_id, instance_id=in_id, image_name=name, **kwargs)
            res = cli.create_image(req)
            return res.to_map()['body']

