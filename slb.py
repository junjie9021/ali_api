from .client import SLBClient
from alibabacloud_slb20140515 import models
from pprint import pprint

class SLB(SLBClient):
    """负载均衡器接口
    文档: https://next.api.alibabacloud.com/api/Slb/2014-05-15
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, region_id, **kwargs):
        # 默认获取全部的
        with self as cli:
            req = models.DescribeLoadBalancersRequest(region_id=region_id, **kwargs)
            res = cli.describe_load_balancers(req)
            return res.to_map()['body']

    def create(self, region_id, name, master_zone_id, slave_zone_id,
                    address_type='internet', 
                    load_balancer_spec='slb.s2.small', 
                    address_ipversion='ipv4', 
                    pay_type='PayOnDemand',
                    **kwargs):
        with self as cli:
            req = models.CreateLoadBalancerRequest(
                    region_id=region_id,
                    load_balancer_name=name,
                    address_type=address_type,
                    load_balancer_spec=load_balancer_spec,
                    address_ipversion=address_ipversion,
                    pay_type=pay_type,
                    **kwargs
                )
            res = cli.create_load_balancer(req)
            return res.to_map()['body']

    def delete(self, region_id, slb_id):
        with self as cli:
            req = models.DeleteLoadBalancerRequest(region_id=region_id, load_balancer_id=slb_id)
            res = cli.delete_load_balancer(req)
            return res.to_map()['body']

    def get_health_status(self, region_id, slb_id, **kwargs):
        with self as cli:
            req = models.DescribeHealthStatusRequest(region_id=region_id, load_balancer_id=slb_id, **kwargs)
            res = cli.describe_health_status(req)
            return res.to_map()['body']

    def add_tag(self, region_id, slb_id, tags):
        if isinstance(tags, str):
            tags = [tags]
        with self as cli:
            req = models.AddTagsRequest(region_id=region_id, load_balancer_id=slb_id, tags=tags)
            res = cli.add_tags(req)
            return res.to_map()['body']

    def get_zone_id(self, region_id):
        # 获取可用区id
        with self as cli:
            req = models.DescribeZonesRequest(region_id=region_id)
            res = cli.describe_zones(req)
            return res.to_map()['body']

    def get_vserver_groups(self, region_id, slb_id, **kwargs):
        """查询服务器组列表"""
        with self as cli:
            req = models.DescribeVServerGroupsRequest(region_id=region_id, load_balancer_id=slb_id, **kwargs)
            res = cli.describe_vserver_groups(req)
            return res.to_map()['body']

    def get_vserver_group_detail(self, region_id, vserver_group_id):
        """查询服务器组的详细信息"""
        with self as cli:
            req = models.DescribeVServerGroupAttributeRequest(region_id=region_id, vserver_group_id=vserver_group_id)
            res = cli.describe_vserver_group_attribute(req)
            return res.to_map()['body']

    def delete_vserver_group(self, region_id, vserver_group_id):
        with self as cli:
            req = models.DeleteVServerGroupRequest(region_id=region_id, vserver_group_id=vserver_group_id)
            res = cli.delete_vserver_group(req)
            return res.to_map()['body']

    def create_vserver_group(self, region_id, slb_id, name, backend_servers=None):
        """添加后端服务器组并向指定的后端服务器组中添加后端服务器"""
        with self as cli:
            if backend_servers:
                req = models.CreateVServerGroupRequest(region_id=region_id, load_balancer_id=slb_id, vserver_group_name=name)
            else:
                req = models.CreateVServerGroupRequest(region_id=region_id, load_balancer_id=slb_id, vserver_group_name=name, backend_servers=backend_servers)
            res = cli.create_vserver_group(req)
            return res.to_map()['body']

    def remove_backend_servers(self, region_id, slb_id, backend_servers: str):
        """移除后端服务器
        backend_servers格式 [{"ServerId":"i-2zej4lxhjoq***", "Type": "ecs","Weight":"100"}]"""
        with self as cli:
            req = models.RemoveBackendServersRequest(region_id=region_id, load_balancer_id=slb_id, backend_servers=backend_servers)
            res = cli.remove_backend_servers(req)
            return res.to_map()['body']

    def add_backend_servers(self, region_id, slb_id, backend_servers: str):
        """添加后端服务器"""
        with self as cli:
            req = models.AddBackendServersRequest(region_id=region_id, load_balancer_id=slb_id, backend_servers=backend_servers)
            res = cli.add_backend_servers(req)
            return res.to_map()['body']


    def create_listener(self, region_id, slb_id, vserver_group_id, listener_port, bandwidth=-1,
                        health_check_interval=2, established_timeout=900, scheduler='tch',
                        health_check_connect_timeout=5, **kwargs):
        """创建TCP监听"""
        with self as cli:
            req = models.CreateLoadBalancerTCPListenerRequest(
                        region_id=region_id, 
                        load_balancer_id=slb_id, 
                        vserver_group_id=vserver_group_id,
                        listener_port=int(listener_port), 
                        scheduler=scheduler,
                        bandwidth=bandwidth,
                        health_check_interval=2,
                        established_timeout=900,
                        health_check_connect_timeout=5,
                        **kwargs)
            res = cli.create_load_balancer_tcplistener(req)
            return res.to_map()['body']

    def update_listener(self, region_id, slb_id, vserver_group_id, listener_port, bandwidth=-1,
                    health_check_interval=2, established_timeout=900, scheduler='tch',
                    health_check_connect_timeout=5, **kwargs):
        """修改TCP监听"""
        with self as cli:
            req = models.SetLoadBalancerTCPListenerAttributeRequest(
                        region_id=region_id, 
                        load_balancer_id=slb_id, 
                        vserver_group_id=vserver_group_id,
                        listener_port=int(listener_port), 
                        scheduler=scheduler,
                        bandwidth=bandwidth,
                        health_check_interval=2,
                        established_timeout=900,
                        health_check_connect_timeout=5,
                        **kwargs)
            res = cli.set_load_balancer_tcplistener_attribute(req)
            return res.to_map()['body']


    def delete_listener(self, region_id, slb_id, listener_port, **kwargs):
        with self as cli:
            req = models.DeleteLoadBalancerListenerRequest(region_id, load_balancer_id=slb_id,  listener_port=int(listener_port))
            res = cli.delete_load_balancer_listener(req)
            return res.to_map()['body']

    def start_listener(self, region_id, slb_id, listener_port, **kwargs):
        """启动监听"""
        with self as cli:
            req = models.StartLoadBalancerListenerRequest(region_id=region_id, load_balancer_id=slb_id, listener_port=int(listener_port))
            res = cli.start_load_balancer_listener(req)
            return res.to_map()['body']

    def stop_listener(self, region_id, slb_id, listener_port, **kwargs):
        """启动监听"""
        with self as cli:
            req = models.StopLoadBalancerListenerRequest(region_id=region_id, load_balancer_id=slb_id, listener_port=int(listener_port))
            res = cli.stop_load_balancer_listener(req)
            return res.to_map()['body']

    def get_listeners(self, region_id, type='tcp', slb_id=None):
        """查询负载均衡监听列表详情,默认tcp协议"""
        with self as cli:
            req = models.DescribeLoadBalancerListenersRequest(region_id=region_id, listener_protocol=type)
            res = cli.describe_load_balancer_listeners(req)
            return res.to_map()['body']

    def __str__(self):
        # 返回产品类型,用于endpoint
        return 'slb'
