
"""
This script expects that the following environment vars are set:
DJANGO_API_ENDPOINT
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID

"""
import os
import json
import traceback
#import configparser
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import DiskCreateOption
from azure.mgmt.resource import SubscriptionClient
from msrestazure.azure_exceptions import CloudError
import requests 
from datetime import datetime
import logging


API_ENDPOINT = os.environ['DJANGO_API_ENDPOINT']

debug_mode = False
quick_mode = True

#logging.basicConfig(filename='loadvmdata.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
#logging.basicConfig(level=logging.INFO,filename='logs/loadvmdata.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO,filename='logs/loadvmdata.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
#logging.basicConfig(level=logging.INFO)



################################
def get_azure_cred():
    """Get credential

    :param cred_file: the file containing the Azure credential info
    :param subscription_id: Azure subscription id
    """

    credentials = ServicePrincipalCredentials(

      client_id = os.environ['AZURE_CLIENT_ID'],
      secret = os.environ['AZURE_CLIENT_SECRET'],
      tenant = os.environ['AZURE_TENANT_ID']
    )
    return credentials

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
    """Get the primary ip address of a VM

    :param network: the NetworkManagementClient object
    :param vm: the VirtualMachine object
    """
   
    primary_nic = vm.network_profile.network_interfaces[0].id.split('/')[-1:][0]
    primary_nic_rg = vm.network_profile.network_interfaces[0].id.split('/')[4]
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

########################################################
def get_vm_all_ip(vm, network_client):
    """Get the all ip addresses of a VM

    :param network: the NetworkManagementClient object
    :param vm: the VirtualMachine object
    """
    all_ips =[]
    for interface in vm.network_profile.network_interfaces:
        name=" ".join(interface.id.split('/')[-1:])
        sub="".join(interface.id.split('/')[4])

        try:
            thing=network_client.network_interfaces.get(sub, name).ip_configurations

            for x in thing:
                #print(x.private_ip_address)
                all_ips.append(x.private_ip_address)

        except:
            print("Unable to get the IP address for the machine "+ name)    

    return all_ips

##################################################    
def send_rest_req(vm_info,API_URL):
    """Send a HTTP REST request to the API server to update the VM inventory

    :param vm_info: the info of a vm in a dictionary format
    :param API_URL: the API server endpoint
    """    
    headers = {'Content-type': 'application/json'}
    API_URL = API_ENDPOINT +"vm/"+ vm_info['name'] + "/"
    r = requests.get(url = API_URL) 
    if r.headers['Content-Length'] == "2":
        logging.info(str(datetime.now())+" The record does not exist...creating " + vm_info['name'])
        CREATE_URL = API_ENDPOINT + "create/"
        #print(CREATE_URL+" : "+ json.dumps(vm_info))
        r = requests.post(url = CREATE_URL, data = json.dumps(vm_info), headers=headers,verify=False) 
    else:
        logging.info(str(datetime.now())+' The record exists...updating ' + vm_info['name'])
        UPDATE_URL = API_ENDPOINT + "update/" + vm_info['name']        
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
    
    if resource_group == None:
        for rg in get_resource_groups(credentials,subscription_id):
        # List VMs in subscription
            
            for vm in compute_client.virtual_machines.list(rg,expand='instanceView'):
            #for vm in compute_client.virtual_machines.list_all():
            #for vm in compute_client.virtual_machines.list('SEA-GIS-CLOUD-IMAGES'):
                #name = vm['name']
                #print('###Loading..'+ vm.name)
                logging.info('### Scanning VM..'+ vm.name)
                try:
                    hw = vm.hardware_profile  
                    storage = vm.storage_profile 
                    avset = vm.availability_set.id.split('/')[-1:][0] if vm.availability_set is not None  else str('NA')
                    #avset = vm.availability_set.id.split('/')[-1:][0]
                    #os = vm.os_profile
                    
                    instance_view =get_vm(compute_client,rg,vm.name).instance_view
                    #os = instance_view.os_name
                    os = instance_view.os_name if instance_view.os_name is not None else str('NA')
                    status = instance_view.statuses[1].display_status
                    disks =[disk.name for disk in instance_view.disks]
                    disks = ','.join(disks)
                    primary_ip = get_vm_primary_ip(network_client,vm)
                    secondary_ips = [ip for ip in get_vm_all_ip(vm,network_client) if ip == primary_ip]
                    tags = json.dumps(vm.tags)

                    vm_info = {
                        'subscription': subscriptions[subscription_id],
                        'resource_group':rg,
                        'name':vm.name,
                        'primary_ip_address':primary_ip,
                        'secondary_ip_addresses': ','.join(secondary_ips),
                        'location':vm.location,
                        'vm_size':hw.vm_size,
                        'os_disk':storage.os_disk.name,
                        'os_disk_size':storage.os_disk.disk_size_gb,
                        'os':os,
                        'status':status,
                        'disks':disks,
                        'AVSet':avset,
                        'tags':tags
                        }
                    send_rest_req(vm_info,API_ENDPOINT)    
                    if debug_mode == True:
                        #print(json.dumps(vm_info,indent=4))   
                        logging.debug(json.dumps(vm_info,indent=4))         
                except Exception as e:
                    #print('#### Error in retrieving info for '+ vm.name+ '#### ==> ' + str(e))
                    logging.error('#### Error in retrieving info for '+ vm.name+ '#### ==> ' + str(e))

    else:        
        try:
            for vm in compute_client.virtual_machines.list(resource_group,expand='instanceView'):
                #print('###Loading..'+ vm.name)
                logging.info('### Scanning VM..'+ vm.name)
                try:
                    hw = vm.hardware_profile  
                    storage = vm.storage_profile                     
                    avset = vm.availability_set.id.split('/')[-1:][0] if vm.availability_set is not None  else str('NA')
                    #os = vm.os_profile
                    
                    instance_view =get_vm(compute_client,resource_group,vm.name).instance_view
                    #os = instance_view.os_name
                    os = instance_view.os_name if instance_view.os_name is not None else str('NA')
                    status = instance_view.statuses[1].display_status
                    disks =[disk.name for disk in instance_view.disks]
                    disks = ','.join(disks)
                    primary_ip = get_vm_primary_ip(network_client,vm)
                    secondary_ips = [ip for ip in get_vm_all_ip(vm,network_client) if ip == primary_ip]
                    tags = json.dumps(vm.tags)
                    vm_info = {
                        'subscription': subscriptions[subscription_id],
                        'resource_group':resource_group,
                        'name':vm.name,
                        'primary_ip_address':primary_ip,
                        'secondary_ip_addresses': ','.join(secondary_ips),
                        'location':vm.location,
                        'vm_size':hw.vm_size,
                        'os_disk':storage.os_disk.name,
                        'os_disk_size':storage.os_disk.disk_size_gb,
                        'os':os,
                        'status':status,
                        'disks':disks,
                        'AVSet':avset,
                        'tags':tags
                        }
                    #vm_list[vm.name] = (vm_info)
                    send_rest_req(vm_info,API_ENDPOINT)
                    if debug_mode == True:
                        #print(json.dumps(vm_info,indent=4)) 
                        logging.debug(json.dumps(vm_info,indent=4))          
                except Exception as e:
                    #print('#### Error in retrieving info for '+ vm.name+ '#### ==> ' + str(e))
                    logging.error('#### Error in retrieving info for '+ vm.name+ '#### ==> ' + str(e))
        except Exception as e:
            #print('Error in finding the resource group: ' + resource_group)
            logging.error('Error in finding the resource group: ' + resource_group)
    return vm_list

        

if __name__ == "__main__":
    cred = get_azure_cred()
    #load_vm(cred,subid,'EAS-HCS-DEV-01')
    #get_vm_list(cred,subid,'EAS-HCS-DEV-01')
    subscriptions_list = get_subscriptions(cred)
    for sub in subscriptions_list.keys():
        load_vm(cred,sub)