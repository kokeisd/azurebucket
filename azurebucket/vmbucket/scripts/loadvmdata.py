# https://buildmedia.readthedocs.org/media/pdf/azure-sdk-for-python/v2.0.0rc6/azure-sdk-for-python.pdf
# https://docs.microsoft.com/en-us/python/api/azure-mgmt-compute/azure.mgmt.compute.v2019_04_01?view=azure-python
"""Create and manage virtual machines.

This script expects that the following environment vars are set:

AZURE_TENANT_ID: your Azure Active Directory tenant id or domain
AZURE_CLIENT_ID: your Azure Active Directory Application Client ID
AZURE_CLIENT_SECRET: your Azure Active Directory Application Secret
AZURE_SUBSCRIPTION_ID: your Azure Subscription Id
"""
import os
import json
import traceback
import configparser

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import DiskCreateOption
from azure.mgmt.resource import SubscriptionClient

from msrestazure.azure_exceptions import CloudError
import requests 


AZURE_TENANT_ID = '5d3e2773-e07f-4432-a630-1a0f68a28a05'
AZURE_CLIENT_ID = '03828b49-95e3-4856-975f-8e12a6a50a73'
AZURE_CLIENT_SECRET = 'djd5hzSLRcaK0jTJjl1+xKPGQcRxUXiYDkuB0fq+ZjY='
AZURE_SUBSCRIPTION_ID = '96bdec4d-beee-4317-8e6d-06fc6b76cb79'

API_ENDPOINT = "http://10.235.17.55:8000/vmbucket/"

debug_mode = True
quick_mode = True

CRED_FILE = 'cred.cfg'

################################
def get_azure_cred(cred_file):
    """Get credential

    :param cred_file: the file containing the Azure credential info
    :param subscription_id: Azure subscription id
    """
    config = configparser.ConfigParser()
    config.read(cred_file)

    subscription_id = str(config['DEFAULT']['azure_subscription_id'])
    ##print('*****'+subscription_id)
    credentials = ServicePrincipalCredentials(
        client_id=config['DEFAULT']['azure_client_id'],
        secret=config['DEFAULT']['azure_client_secret'],
        tenant=config['DEFAULT']['azure_tenant_id']
    )
    return credentials, subscription_id

#####################
def get_resource_groups(credentials,subscription_id):
    """Get list of resources group

    :param credentials: 
    :param subscription_id: 
    """
    resource_client = ResourceManagementClient(credentials, subscription_id)
    rglist = []
    rgs = resource_client.resource_groups.list()

    for resource_group in rgs:
        rglist.append(resource_group.name)
    
    return rglist


#####################################
def get_vm(compute, resource_group, instance_name):
    """Get the details of a VM

    :param credentials: 
    :param subscription_id: 
    """
    return compute.virtual_machines.get(
        resource_group, instance_name, expand='instanceView')     

##################
def get_nic(network, resource_group, name):
    try:
        return network.network_interfaces.get(resource_group, name)
    except CloudError:
        raise exception.PortNotFound(port_id=name)

#################
def get_vm_primary_ip(network,vm):
    """Get the details of a VM

    :param network: the NetworkManagementClient object
    :param vm: the VirtualMachine object
    """
   
    primary_nic = vm.network_profile.network_interfaces[0].id.split('/')[-1:][0]
    primary_nic_rg = vm.network_profile.network_interfaces[0].id.split('/')[4]
    #print(vm.network_profile.network_interfaces[0].id)
    #print(primary_nic_rg, primary_nic)
    ip_configs=network.network_interfaces.get(primary_nic_rg, primary_nic).ip_configurations

    for ip_conf in ip_configs:
        if ip_conf.primary is True:  
            return ip_conf.private_ip_address

########################################################
def get_subscriptions(credentials):
    """Get the list of subscriptions 

    :param credentials: 
    """    
    subs_dict={}
    subscriptionClient = SubscriptionClient(credentials)
    for subscription in subscriptionClient.subscriptions.list():
        subs_dict[subscription.subscription_id] = subscription.display_name
        #print(subscription.subscription_id)
    return subs_dict

##################################################    
def send_rest_req(vm_info,API_URL):
    headers = {'Content-type': 'application/json'}
    API_URL = API_ENDPOINT + vm_info['name'] + "/"
    r = requests.get(url = API_URL) 
    if r.headers['Content-Length'] == "2":
        print("The record does not exist...creating " + vm_info['name'])
        CREATE_URL = API_ENDPOINT + "create/"
        print(CREATE_URL+" : "+ json.dumps(vm_info))
        r = requests.post(url = CREATE_URL, data = json.dumps(vm_info), headers=headers,verify=False) 
    else:
        print('The record exists...updating ' + vm_info['name'])
        UPDATE_URL = API_ENDPOINT + vm_info['name'] + "/update/"
        print(UPDATE_URL+" : " +json.dumps(vm_info))
        r = requests.put(url = UPDATE_URL, data = json.dumps(vm_info), headers=headers,verify=False)               


############################
def load_vm(credentials,subscription_id,resource_group =None):
    """Get the list of VMs in a subscription

    :param credentials: 
    :param subscription_id: 
    """
    #credentials, subscription_id = get_azure_cred()
    #resource_client = ResourceManagementClient(credentials, subscription_id)
    compute_client = ComputeManagementClient(credentials, subscription_id)
    network_client = NetworkManagementClient(credentials, subscription_id)

    vm_list ={}
    # print('\nList VMs in subscription')

    subscriptions = get_subscriptions(credentials)
    #headers = {'Content-type': 'application/json'}
    
    if resource_group == None:
        for rg in get_resource_groups(credentials,subscription_id):
        # List VMs in subscription
            
            for vm in compute_client.virtual_machines.list(rg,expand='instanceView'):
            #for vm in compute_client.virtual_machines.list_all():
            #for vm in compute_client.virtual_machines.list('SEA-GIS-CLOUD-IMAGES'):
                #name = vm['name']
                print('###Loading..'+ vm.name)
                try:
                    hw = vm.hardware_profile  
                    storage = vm.storage_profile 
                    #avset = vm.availability_set.id.split('/')[-1:][0]
                    #os = vm.os_profile
                    instance_view =get_vm(compute_client,rg,vm.name).instance_view
                    #os = instance_view.os_name
                    os = instance_view.os_name if instance_view.os_name is not None else str('NA')
                    status = instance_view.statuses[1].display_status
                    disks =[disk.name for disk in instance_view.disks]
                    disks = ','.join(disks)
                    #disks = disks + disk.name for disk in instance_view.disks

                    primary_ip = get_vm_primary_ip(network_client,vm)
                    tags = json.dumps(vm.tags)

                    vm_info = {
                        'subscription': subscriptions[subscription_id],
                        'resource_group':rg,
                        'name':vm.name,
                        'primary_ip':primary_ip,
                        'location':vm.location,
                        'vm_size':hw.vm_size,
                        'os_disk':storage.os_disk.name,
                        'os_disk_size':storage.os_disk.disk_size_gb,
                        'os':os,
                        'status':status,
                        'disks':disks,
                       # 'AVSet':avset,
                        'tags':tags
                        }
                    send_rest_req(vm_info,API_ENDPOINT)    
                    if debug_mode == True:
                        print(json.dumps(vm_info,indent=4))            
                except:
                    print('#### Error in retrieving info for '+ vm.name+ '####')

    else:        
        for vm in compute_client.virtual_machines.list(resource_group,expand='instanceView'):
            print('###Loading..'+ vm.name)
            try:
                hw = vm.hardware_profile  
                storage = vm.storage_profile 
                avset = vm.availability_set.id.split('/')[-1:][0]
                #os = vm.os_profile
                instance_view =get_vm(compute_client,resource_group,vm.name).instance_view
                #os = instance_view.os_name
                os = instance_view.os_name if instance_view.os_name is not None else str('NA')
                status = instance_view.statuses[1].display_status
                disks =[disk.name for disk in instance_view.disks]
                disks = ','.join(disks)
                #disks = "".join(disk.name) for disk in instance_view.disks

                primary_ip = get_vm_primary_ip(network_client,vm)

                tags = json.dumps(vm.tags)
                vm_info = {
                    'subscription': subscriptions[subscription_id],
                    'resource_group':resource_group,
                    'name':vm.name,
                    'primary_ip':primary_ip,
                    'location':vm.location,
                    'vm_size':hw.vm_size,
                    'os_disk':storage.os_disk.name,
                    'os_disk_size':storage.os_disk.disk_size_gb,
                    'os':os,
                    'status':status,
                    'disks':disks,
                    'AVSet':avset,
                    #'tags':vm.tags
                    'tags':tags
                    }
                #vm_list[vm.name] = (vm_info)
                send_rest_req(vm_info,API_ENDPOINT)
                if debug_mode == True:
                    print(json.dumps(vm_info,indent=4))  
            except:
                print('#### Error in retrieving info for '+ vm.name+ '####')


    return vm_list

        






if __name__ == "__main__":
    cred,subid = get_azure_cred(CRED_FILE)
    # GUIprint(get_vm_list(cred,subid,'EAS-HCS-DEV-01'))
    #get_vm_list(cred,subid,'EAS-HCS-DEV-01')
    subscriptions_list = get_subscriptions(cred)
    for sub in subscriptions_list.keys():
        load_vm(cred,sub)