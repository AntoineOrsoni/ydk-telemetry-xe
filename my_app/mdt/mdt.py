import yaml
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_mdt_cfg as mdt_cfg
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_mdt_oper as mdt_oper

class Device:

    def __init__(self, device_id):
        device_list = yaml.safe_load(open("./env_info/device_info.yaml", "r"))
        self.id = device_id
        self.name = device_list[device_id]["name"]
        self.username = device_list[device_id]["username"]
        self.password = device_list[device_id]["password"]
        self.mgmt_ip = device_list[device_id]["mgmt_ip"]
        self.ssh_port = device_list[device_id]["ssh_port"]
        self.netconf_port = device_list[device_id]["netconf_port"]

    def get_netconf_provider(self):
        provider = NetconfServiceProvider(address=self.mgmt_ip,
                                          port=self.netconf_port,
                                          username=self.username,
                                          password=self.password)
        return provider

    def create_entity(self, provider, entity):
        crud = CRUDService()

        return crud.create(provider, entity)

    def read_entity(self, provider, entity):
        crud = CRUDService()

        return crud.read(provider, entity)

    def delete_entity(self, provider, entity):
        crud = CRUDService()

        return crud.delete(provider, entity)

class MDT(Device):

    def __init__(self, device_id):
        super().__init__(device_id)

    # TODO get_list_subscription
    #   return subscription_id
    #   -> (create the next available subscription_id)

    def create_mdt_config(self, subscription_id, subscription_period, subscription_xpath):

        mdt_config_data = mdt_cfg.MdtConfigData()

        mdt_config_data.mdt_subscription.append(self.create_mdt_subscription(subscription_id,
                                                                             subscription_period,
                                                                             subscription_xpath))

        return self.create_entity(self.get_netconf_provider(), mdt_config_data)

    def create_mdt_subscription(self, subscription_id, subscription_xpath, subscription_period=500):

        mdt_subscription = mdt_cfg.MdtConfigData.MdtSubscription()

        mdt_subscription.subscription_id = subscription_id

        mdt_subscription.base.stream = "yang-push"
        mdt_subscription.base.encoding = "encode-kvgpb"
        mdt_subscription.base.period = subscription_period
        mdt_subscription.base.xpath = subscription_xpath

        mdt_receiver_info = yaml.safe_load(open("./env_info/mdt_receiver_info.yaml", "r"))
        mdt_receivers = mdt_cfg.MdtConfigData.MdtSubscription.MdtReceivers()
        mdt_receivers.address = mdt_receiver_info[self.id]["address"]
        mdt_receivers.port = mdt_receiver_info[self.id]["port"]
        mdt_receivers.protocol = mdt_receiver_info[self.id]["protocol"]

        mdt_subscription.mdt_receivers.append(mdt_receivers)

        return mdt_subscription

    def create_mdt_config_cpu(self, subscription_id, subscription_period=500):
        subscription_xpath = "/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds"

        return self.create_mdt_config(subscription_id, subscription_xpath, subscription_period)

    def create_mdt_config_memory(self, subscription_id, subscription_period=500):
        subscription_xpath = "/memory-ios-xe-oper:memory-statistics/memory-statistic"

        return self.create_mdt_config(subscription_id, subscription_xpath, subscription_period)

    def read_mdt_subscription_id(self, subscription_id):
        mdt_subscription = mdt_oper.MdtOperData.MdtSubscriptions()
        mdt_subscription.subscription_id = subscription_id

        return self.read_entity(self.get_netconf_provider(), mdt_subscription)

    # TODO: doesn't work yet.
    def read_mdt_subscription_list(self):

        list_id = []
        mdt_subscription = mdt_oper.MdtOperData()

        mdt_subscription_list = self.read_entity(self.get_netconf_provider(), mdt_subscription)

        for subscription in mdt_subscription_list.mdt_subscriptions:
            print(mdt_subscription_list.mdt_subscriptions[subscription])
            list_id.append(subscription)

        return list_id

    def delete_mdt_config(self, subscription_id):
        mdt_config_data = mdt_cfg.MdtConfigData()

        mdt_config_data.mdt_subscription.append(self.delete_mdt_subscription_id(subscription_id))

        return self.delete_entity(self.get_netconf_provider(), mdt_config_data)


    def delete_mdt_subscription_id(self, subscription_id):
        mdt_subscription = mdt_cfg.MdtConfigData.MdtSubscription()
        mdt_subscription.subscription_id = subscription_id

        return mdt_subscription


