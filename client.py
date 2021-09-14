from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526.client import Client as Ecs # ecs client
from alibabacloud_slb20140515.client import Client as Slb # slb client
from alibabacloud_vpc20160428.client import Client as Vpc # vpc client

__all__ = ('ECSClient', 'VPCClient', 'SLBClient')


class Client:
    """阿里云client api接口"""
    def __init__(self, ak, sk, endpoint):
        # 注意: 每个产品的endpoint 不同，如 ecs的ecs.[区域id].aliyuncs.com
        self.config = open_api_models.Config(
            access_key_id=ak,
            access_key_secret=sk
            )
        self.endpoint = endpoint
        self.client = None

    def _set_client(self, type):
        # type: 阿里云产品类型所属client
        if self.client is not None:
            return self.client
        self.config.endpoint = self.endpoint
        self.client = type(self.config)
        return self.client


class ECSClient(Client):
    """ECS client"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_client(self):
        return self._set_client(Ecs)

    def __enter__(self):
        if self.client is not None:
            raise RuntimeError('Already connected')
        return self.get_client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client = None


class VPCClient(Client):
    """VPC client"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_client(self):
        return self._set_client(Vpc)

    def __enter__(self):
        if self.client is not None:
            raise RuntimeError('Already connected')
        return self.get_client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client = None


class SLBClient(Client):
    """SLB client"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_client(self):
        return self._set_client(Slb)

    def __enter__(self):
        if self.client is not None:
            raise RuntimeError('Already connected')
        return self.get_client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client = None