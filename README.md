**Work in progress**

Easily create a YDK project with Dockerfile from this template.

The logic is stored in `my_app/mdt.py`.

## Instancing the MDT Class

You first need to create an instance of the class `MDT`.

`my_mdt = MDT(device_id)`

`device_id` is the index of the device in `/my_app/env_info/device_info.yaml`

## Creating a subscription

`create_mdt_config(self, subscription_id, subscription_period, subscription_xpath)`

This is a method of the class MDT, sub-class of Device.
You can create your own subscription. You need to provide:
* `subscription_id`: the `id` of the subscription (verify that the `id` is not already in use on the device)
* `subscription_period`: the `period` between two dial-out from the device (in seconds)
* `subscription_xpath`: the `xpath` of the leaf you want to subscribe.

### Creating a subscription for memory

`create_mdt_config_memory(self, subscription_id, subscription_period=500)`

This is a method of the class MDT, sub-class of Device.
You can create your a pre-filled subscription, to monitor the memory of the device. You need to provide:
* `subscription_id`: the `id` of the subscription (verify that the `id` is not already in use on the device)
* `subscription_period`: the `period` between two dial-out from the device (in seconds). Default value: 500 seconds.

### Creating a subscription for CPU

`create_mdt_config_cpu(self, subscription_id, subscription_period=500)`

This is a method of the class MDT, sub-class of Device.
You can create your a pre-filled subscription, to monitor the CPU of the device. You need to provide:
* `subscription_id`: the `id` of the subscription (verify that the `id` is not already in use on the device)
* `subscription_period`: the `period` between two dial-out from the device (in seconds). Default value: 500 seconds.

## Reading a subscription

`read_mdt_subscription_id(self, subscription_id)`

This is a method of the class MDT, sub-class of Device.
You can read a subscription. You need to provide:
* `subscription_id`: the `id` of the subscription.

## Deleting a subscription

Bug: delete_mdt_config(subscription_id) deletes all subscriptions, not only the specified id.


`read_mdt_config(self, subscription_id)`

This is a method of the class MDT, sub-class of Device.
You can delete a subscription. You need to provide:
* `subscription_id`: the `id` of the subscription.

## TODO:

* delete_mdt_config() deletes all subscriptions, not only the specified id.
* create a REST API.
* verify is the NETCONF_provider is still available, if yes, reuse it.
* integrate with a TIG (Telegraf, Influxdb, Grafana) container.
* list all subscription_id for a device.
