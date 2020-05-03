from mdt.mdt import Device, MDT
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_mdt_oper as mdt_oper
from ydk.filters import YFilter

mdt_1 = MDT(0)
# mdt_1.create_mdt_config_memory(104)

mdt_subscription = mdt_oper.MdtOperData.MdtSubscriptions()
# mdt_subscription_list = mdt_1.read_entity(mdt_1.get_netconf_provider(), mdt_subscription)

# TODO: make a REST API