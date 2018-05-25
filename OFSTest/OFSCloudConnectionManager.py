#!/usr/bin/python


#import os
import time
import re
from pprint import pprint
from datetime import datetime, timedelta

## 
# @class OFSCloudConnectionManager
#
# @brief This class manages the Cloud connection. It has no awareness of OFSTestNodes or the OFSTestNetwork.
# This class is an abstract class. The implementation for different cloud APIs (OpenStack Nova, Amazon EC2) should be written as subclasses. 
#

class OFSCloudConnectionManager(object):
  
    ##
    #
    # @fn __init__(self,cloud_config_file=None,region_name=None):
    #
    # Initialization
    #
    # @param self The object pointer
    # @param cloud_config_file Path to cloudrc.sh file.
    # @param region_name Name of cloud region to connect to.
    #

    
    def __init__(self):
        
        ##
        # @var self.cloud_instance_names
        # @brief Dictionary of Cloud instance names
        self.cloud_instance_names = {}
        
        # @var self.cloud_instance_list
        # @brief Dictionary of Cloud instances
        self.cloud_instance_list = {}
        
        # @var self.cloud_image_list
        # @brief List of all available images
        self.cloud_image_list = None
        
        # @var self.cloud_key_list
        # @brief List of all available keys (not used)
        self.cloud_key_list = None
        
        # @var self.cloud_region_name
        # @brief Cloud region name. Required to connect.
        self.cloud_is_secure = False
        
        # @var self.cloud_is_secure
        # @brief Is this http or https?
        self.cloud_instance_key = None
               
        # @var String self.cloud_instance_key
        # @brief Name of key (in Cloud) used to access instance via SSH
        self.cloud_instance_key_location = None
        
    ##
    #
    # @fn readCloudConfigFile(self,filename):
    #
    # Reads relevant values from configuration file.
    #
    # @param self The object pointer
    #
    # @param filename Path to configuration file
    #
            
    
    def readCloudConfigFile(self,filename):
        pass


    ##
    #
    # @fn readCloudPasswordFile(self,filename):
    #
    # Reads relevant values from password file. This file contains the password for nova that is used for the OS_PASSWORD value
    #
    # @param self The object pointer
    #
    # @param filename Path to file
    #
    
    def readCloudPasswordFile(self,filename):
        pass
                
    ##
    #      
    # @fn connect(self,debug): 
    # Gets region info and connects to Cloud. cloud.connection.CloudConnection object should be stored in self.cloud_connection.
    # @param self The object pointer
    # @param debug  Debug level.
    #

    def connect(self,debug=0):
        pass
        

    ##
    #      
    # @fn setCloudKey(self,keyname,keylocation):
    # Sets key name (Cloud) and key location (file) used to create and access Cloud instances.
    # @param self  The object pointer
    # @param keyname Name of key in Cloud
    # @param keylocation Location of .pem file in filesystem.
    #
    #

    def setCloudKey(self,keyname,keylocation):
        self.cloud_instance_key = keyname
        self.cloud_instance_key_location = keylocation

    ##
    # @fn getAllImages(self ):	
    # Get a list of all the Cloud images
    # @param self  The object pointer		
    # @return A list of available Cloud Images	
    #

    def getAllCloudImages(self):
        pass
    ##
    # @fn terminateCloudInstance(self,ip_address)
    # Terminates a running Cloud instance 
    #
    # @param self The object pointer
    # @param	ip_address IP address (internal) of the node.
    #
    # @return 1	Instance not found for that ip address
    # @return 0	Instance terminated.
    #
    #
        
    def terminateCloudInstance(self,ip_address):
        pass


    ##
    # @fn stopCloudInstance(self,ip_address)
    # Stops a running Cloud instance 
    #
    # @param self The object pointer
    # @param    ip_address IP address (internal) of the node.
    #
    # @return 1    Instance not found for that ip address
    # @return 0    Instance terminated.
    #
    #
        
    def stopCloudInstance(self,ip_address):
        pass

    ##
    #
    # @fn createNewCloudInstances(self,number_nodes,image_system,instance_type,subnet_id=None,instance_suffix="",image_id=None,security_group_ids=None,spot_instance_bid=None): 
    # Creates new Cloud instances and returns list of them.
    #
    # @param self The object pointer
    # @param number_nodes  Number of nodes to create
    # @param image_system Image to run. (e.g. "cloud-ubuntu-12.04")
    # @param instance_type Image "flavor" (e.g. "m1.medium")
	# @param subnet_id Id of subnet instance should run on 
    # @param instance_suffix
    # @param image_id Id of image used for the new instances.
    # @param security_group_ids List of security groups for the new instance.
    # @param spot_instance_bid Maximum spot instance bid. Default is automatic bidding. Ignored if not applicable.
    #
    # @return	A list of new instances.
    #		
        
    def createNewCloudInstances(self,number_nodes,image_system=None,instance_type="t2.micro",subnet_id=None,instance_suffix="",image_id=None,security_group_ids=None,spot_instance_bid=None):
        pass

    ##      
    # @fn associateIPAddresses(self,instances[],domain=None):	
    # Creates an new external IP address and associates	with the instances in the array.
    # @param self The object pointer
    # @param instances List of instances to associate
    # @param domain Domain on which to allocate addresses
    # @return A list of the external addresses
    #

    def associateIPAddresses(self,instances=[],domain=None):
        pass
    ##
    #
    # @fn checkCloudConnection(self):	
    # Checks to see if the Cloud connection is available.	Connects if it isn't.
    # @param self The object pointer
    #

    def checkCloudConnection(self):
        pass
    ##
    #
    # @fn getAllCloudInstances(self):	
    # Gets all instances from Cloud connection. Returns a	list of instances.
    # @param self The object pointer
    #
    
    def getAllCloudInstances(self):
        pass
    ##
    #
    # @fn	printAllInstanceStatus(self):	
    # Prints the status of all instances. For debugging.
    # @param self The object pointer
    #
    
    def printAllInstanceStatus(self):
        pass

        
    #
    #
    #	Future functionality
    # 
    #

    def getCloudConfigFromEnvironment(self):
        print "This should be implemented, but isn't."
        
    def manageExistingCloudInstance(self,cloud_node):
        pass
    
    def getCloudInstanceInformation(self,cloud_node):
        # get the Cloud Information for the node
        pass
    
    def deleteCloudInstance(self,cloud_node):
        pass
    
    def hardRebootCloudInstance(self,cloud_node):
        pass
    
    def deleteAllCloudInstances(self):
        pass  
    
    ##
    # @fn createNewCloudNodes(number_nodes,image_name,machine_type,associateip=False,domain=None,,cloud_subnet=None,instance_suffix="",security_group_ids=None,spot_instance_bid=None):
    #
    # Creates new cloud nodes and adds them to network_nodes list.
    #
    #
    #    @param self The object pointer  
    #    @param number_nodes  number of nodes to be created
    #    @param image_name  Name of Cloud image to launch
    #    @param flavor_name  Cloud "flavor" of virtual node
    #    @param associateip  Associate to external ip?
    #    @param domain Domain to associate with external ip
    #    @param cloud_subnet cloud subnet id for primary network interface.
    #    @param instance_suffix
    #    @param security_group_ids List of security group ids for this instance.
    #    @param spot_instance_bid Maximum bid for spot instances. Default is automatic. Ignored if not applicable.
    #
    #    @returns list of new nodes.


    
    def createNewCloudNodes(self,number_nodes,image_name,flavor_name,local_master,associateip=False,domain=None,cloud_subnet=None,instance_suffix="",security_group_ids=None,spot_instance_bid=None):
        pass
        


#     
# def OFSCloudConnectionManager_test_driver():
#     
#     # old_mgr = OFSCloudConnectionManager(cloud_config_file="/home/jburton/Projects/Testing/PyTest/cloud-cred/cloudrc.sh",region_name="nova")
#     my_mgr = OFSCloudConnectionManager(cloud_config_file="/home/jburton/cuer1/cloudrc.sh",region_name="RegionOne")
#     print "Connect to Cloud"
#     #old_mgr.connect(debug=1)
#     my_mgr.connect(debug=1)
#     
#     print "Testing connection"
#     #old_mgr.printAllInstanceStatus()
#     #my_mgr.printAllInstanceStatus()
#     #my_mgr.getAllImages()
#     #my_mgr.deleteOldInstances(days_old=3)
#     #old_mgr.setCloudKey("BuildBot","/home/jburton/buildbot.pem")
#     my_mgr.setCloudKey("BuildBot2","/home/jburton/cuer1/buildbot2.pem")
# 
#     
#     
#     
#         
#     print "Creating Instances"
#     
#     node_list = my_mgr.createNewCloudInstances(number_nodes=1,image_system="cloud-rhel6",type="m1.small")
#         
#     #print my_mgr
#     for node in node_list:
#         my_mgr.terminateCloudInstance(node.ip_address)
# 
# 
# #OFSCloudConnectionManager_test_driver()
