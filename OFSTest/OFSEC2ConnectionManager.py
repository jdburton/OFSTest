#!/usr/bin/python


#import os
from boto import ec2
from datetime import datetime, timedelta
import logging
import os
from pprint import pprint
import re
import time
import sys
import numpy as np

import OFSCloudConnectionManager
import OFSTestRemoteNode

flavors_order = [ 
       'm3.medium',
       'm3.large',
       'c3.large',
       'm3.xlarge',
       'c3.xlarge',
       'r3.xlarge',
       'd2.xlarge',
       'i2.xlarge',
       'm3.2xlarge',
       'c3.2xlarge',
       'r3.2xlarge',
       'd2.2xlarge',
       'i2.2xlarge',
       'c3.4xlarge',
       'r3.4xlarge',
       'd2.4xlarge',
       'i2.4xlarge',
       'c3.8xlarge',
       'r3.8xlarge',
       'd2.8xlarge',
       'i2.8xlarge',
       'm4.10xlarge'
       ]

## 
# @class OFSEC2ConnectionManager
#
# @brief This class manages the EC2 connection. It has no awareness of OFSTestNodes or the OFSTestNetwork.
#
class OFSEC2ConnectionManager(OFSCloudConnectionManager.OFSCloudConnectionManager):
  
    ##
    #
    # @fn __init__(self,ec2_config_file=None,region_name=None):
    #
    # Initialization
    #
    # @param self The object pointer
    # @param ec2_config_file Path to ec2rc.sh file.
    # @param region_name Name of ec2 region to connect to.
    #
    


    
    def __init__(self,cloud_config_file=None,region_name='us-east-1'):
        
        super(OFSEC2ConnectionManager,self).__init__()
        ##
        # @var self.ec2_access_key  
        # @brief EC2 Access key. In ec2rc.sh file.
        self.ec2_access_key = ""
        
        # @var self.ec2_endpoint
        # @brief Endpoint is the hostname. e.g. devstack.clemson.edu
        self.ec2_endpoint = ""
        
        # @var self.ec2_path
        # @brief Path to EC2 on the host (URL = http://host:port/path)
        self.ec2_path = ""
        
        # @var self.ec2_port
        # @brief Port is TCP port.
        self.ec2_port = ""
        
        # @var self.ec2_secret_key
        # @brief EC2 Secret Key. In ec2rc.sh file.
        self.ec2_secret_key = ""
        
        # @var self.ec2_region
        # @brief EC2 region. Received after initial connect.
        self.ec2_region = None
        
        # @var self.ec2_connection
        # @brief The ec2.connection.EC2Connection object.
        self.ec2_connection = None
        
        
        # @var self.ec2_is_secure
        # @brief Is this http or https?
        
        self.ec2_is_secure = False
        
        
        # @var String self.cloud_instance_key
        # @brief Name of key (in EC2) used to access instance via SSH
        self.cloud_instance_key = None
               
        
        # @var String self.cloud_instance_key_location
        # @brief  *.pem ssh key used to access instance.
        self.cloud_instance_key_location = None
        
    
        # @var self.ec2_region_name
        # @brief EC2 region name. Required to connect.
        
        self.ec2_region_name = None
    
        # Default region name is us-east-1
        if region_name is None:
            self.ec2_region_name = "us-east-1"
        else:
            self.ec2_region_name = region_name
        
       
        if cloud_config_file is not None:
            # Read the ec2rc.sh file if provided
            self.readCloudConfigFile(cloud_config_file)
        else:
            # Otherwise, get the configuration from the environment.
            self.getCloudConfigFromEnvironment()
        
    ##
    #
    # @fn readConfigFile(self,filename):
    #
    # Reads relevant values from ec2rc.sh file.
    #
    # @param self The object pointer
    #
    # @param filename Path to ec2rc file
    #
            
    
    def readCloudConfigFile(self,filename):
        
        #open ec2 file
        ec2conf_rc = open(os.path.expandvars(filename),'r')
        
        #Defaults for AWS, N. Virginia
        self.ec2_is_secure = True
        self.ec2_endpoint = "ec2.us-east-1.amazonaws.com"
        self.ec2_port = ""
        self.ec2_path = "/"
        
        
        
        for line in ec2conf_rc:
            if "export EC2_ACCESS_KEY" in line or "export AWS_ACCESS_KEY" in line:
                # check for EC2_ACCESS_KEY
                (export,variable,self.ec2_access_key) = re.split(' |=',line.rstrip())    
            elif "export EC2_SECRET_KEY" in line or "export AWS_SECRET_KEY" in line:
                # check for EC2_SECRET_KEY
                (export,variable,self.ec2_secret_key) = re.split(" |=",line.rstrip())    
                
            elif "export EC2_URL" in line:
                # check for EC2_URL
                
                url_v = re.split(" |=|://|:|/",line.rstrip())
                
                #url_v contains (export,variable,secure,self.ec2_endpoint,port_string,path...)
                
                # is_secure? http = false, https = true
                if url_v[2] == "https":
                    self.ec2_is_secure = True
                else:
                    self.ec2_is_secure = False
                    
                # endpoint is hostname
                self.ec2_endpoint = url_v[3]
                
                # then comes the port, convert to integer
                # TODO: Make this actually parse a URL properly.
                try:
                    self.ec2_port = int(url_v[4])
                except:
                    self.ec2_port = ""
                
                # finally, the path is all elements from 5 to the end
                try:
                    path_v = url_v[5:]
                except:
                    path_v = []
                
                self.ec2_path = '/'.join(path_v)
                
    ##
    #      
    # @fn connect(self,debug): 
    # Gets region info and connects to EC2. ec2.connection.EC2Connection object should be stored in self.ec2_connection.
    # @param self The object pointer
    # @param debug  Debug level.
    #

    def connect(self,debug=0):
        
        msg = "Connecting to EC2/OpenStack region=%s endpoint=%s" % (self.ec2_region_name,self.ec2_endpoint)
        print msg
        logging.info(msg)

        self.ec2_region = ec2.regioninfo.RegionInfo(name=self.ec2_region_name,endpoint=self.ec2_endpoint)

        

        logging.info("EC2 region is %r" % self.ec2_region)
        
        self.ec2_connection = ec2.connection.EC2Connection(aws_access_key_id=self.ec2_access_key,aws_secret_access_key=self.ec2_secret_key,is_secure=self.ec2_is_secure,port=self.ec2_port
        ,debug=debug,region=self.ec2_region,path=self.ec2_path)
        

        logging.info("EC2 connection is %r" % self.ec2_connection)


    ##
    # @fn getAllCloudImages(self ):	
    # Get a list of all the EC2 images
    # @param self  The object pointer		
    # @return A list of available EC2 Images	
    #

    def getAllCloudImages(self,image_ids=None):
        self.checkCloudConnection()        
        self.cloud_image_list = self.ec2_connection.get_all_images(image_ids=image_ids, filters = {'name':'*ofstest*'})
        
        return self.cloud_image_list

    ##
    # @fn terminateCloudInstance(self,ip_address)
    # Terminates a running EC2 instance 
    #
    # @param self The object pointer
    # @param	ip_address IP address (internal) of the node.
    #
    # @return 1	Instance not found for that ip address
    # @return 0	Instance terminated.
    #
    #
        
    def terminateCloudInstance(self,ip_address):
        
        self.checkCloudConnection()
        
        node_instance = next(( i for i in self.cloud_instance_list if i.private_ip_address == ip_address),None)
        
        if node_instance is None:
            self.getAllCloudInstances()
            node_instance = next(( i for i in self.cloud_instance_list if i.private_ip_address == ip_address),None)
        if node_instance is None:
            logging.exception( "Instance at %s not found." % ip_address)
            return 1
            
        # try:
        #     logging.exception( "Releasing external IP address %s" % node_instance.ext_ip_address)
        #     self.ec2_connection.release_address(node_instance.ext_ip_address)
        # except:
        #     logging.exception( "Warning: Could not release external IP Address "+ node_instance.ext_ip_address)
            
        print "Terminating node at %s" % ip_address
        
        try:
            node_instance.terminate()
        except AttributeError:
            # Terminate will throw an AttributeError when it tries to set the status of a terminated instance. Ignore it.
            pass
        return 0
    
    
        ##
    # @fn stopCloudInstance(self,ip_address)
    # Stop a running EC2 instance 
    #
    # @param self The object pointer
    # @param    ip_address IP address (internal) of the node.
    #
    # @return 1    Instance not found for that ip address
    # @return 0    Instance terminated.
    #
    #
        
    def stopCloudInstance(self,ip_address):
        
        self.checkCloudConnection()
        
        node_instance = next(( i for i in self.cloud_instance_list if i.private_ip_address == ip_address),None)
        
        if node_instance is None:
            self.getAllCloudInstances()
            node_instance = next(( i for i in self.cloud_instance_list if i.private_ip_address == ip_address),None)
        if node_instance is None:
            logging.exception( "Instance at %s not found." % ip_address)
            return 1
            
        # try:
        #     logging.exception( "Releasing external IP address %s" % node_instance.ext_ip_address)
        #     self.ec2_connection.release_address(node_instance.ext_ip_address)
        # except:
        #     logging.exception( "Warning: Could not release external IP Address "+ node_instance.ext_ip_address)
            
        print "Stopping node at %s" % ip_address
        
        try:
            node_instance.stop()
        except AttributeError:
            # Terminate will throw an AttributeError when it tries to set the status of a terminated instance. Ignore it.
            pass
        return 0
    
    ##
    #
    # @fn createNewCloudInstances(self,number_nodes,image_name,flavor_name): 
    # Creates new EC2 instances and returns list of them.
    #
    # @param self The object pointer
    # @param number_nodes  Number of nodes to create
    # @param image_name Image to run. (e.g. "cloud-ubuntu-12.04")
    # @param flavor_name Image "flavor" (e.g. "m1.medium")
	# @param subnet_id Id of subnet instance should run on 
    #
    # @return	A list of new instances.
    #		
        
    def createNewCloudInstances(self,number_nodes,image_name=None,flavor_name="t2.micro",subnet_id=None,instance_suffix="",image_id=None,security_group_ids=None,spot_instance_bid=None ):
        self.checkCloudConnection()  
        
        
        # This creates a new instance for the system of a given machine type
        if image_id is None:
            # get the image ID for the operating system
            if self.cloud_image_list is None:
                self.getAllCloudImages()
            
            # now let's find the os name in the image list
            image = next((i for i in self.cloud_image_list if i.name == image_name), None)
            
            if image is None:
                logging.exception( "Image %s Not Found!" % image_name)
                return None
            
            image_id = image.id
           
        else:
            image_ids = [ image_id ]
            # get the image ID for the operating system

            if self.cloud_image_list is None:
                self.getAllCloudImages(image_ids)
                
            # now let's find the image_id name in the image list
            image = next((i for i in self.cloud_image_list if i.id == image_id), None)

            if image is None:
                logging.exception( "Image %s Not Found!" % image_id)
                return None
            
            image_name = image.name
        
        reservation = None
        new_instances = []
        count = 0
        
        if spot_instance_bid.lower() == "auto":
            
            days_back = 14
            start = datetime.now()-timedelta(days=days_back)
            end = datetime.now()
            next_token = None
            
            set_max = 0
            prices = []
            fallback2standard = False

            product_description = "Linux/UNIX (Amazon VPC)"
            
            if "sles" in image_name: 
                product_description = "SUSE Linux (Amazon VPC)"
                
            try:    
                while count < 30:
                    history = self.ec2_connection.get_spot_price_history(start_time=start.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), end_time=end.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), instance_type=flavor_name, product_description=product_description,next_token=next_token)
                    prices = prices + [price.price for price in history]
                    next_token = history.next_token
                    count += 1
                    # if we are at the end of the set, the number of records returned will be less than 1000.
                    if len(history) < 1000:
                        break
                        
                n = len(prices)
                current_price = max(prices[:3])
                print "Current price for %s instances is %r per instance-hour" % (flavor_name,current_price)
    
                std_dev = np.std(prices)
                mean = np.mean(prices)
                max_bid = mean + 2*std_dev
                
                # Bid 2 standard deviations over the mean. 
                calculated_bid = max_bid
                print "Maximum automatic bid %r is 2 std_dev over mean of %r spot prices over %d days" % (calculated_bid,n,days_back)
                
                #print "n = %r, now = %r, Mean = %r, std_dev = %r, bid (2 stdev) = %r, bid (2.5 stdev) = %r, bid (3 stddev) = %r" % (n,now,mean,std_dev,mean+(2*std_dev),mean+(2.5*std_dev),mean+(3*std_dev))
                spot_instance_bid = str(calculated_bid)
                                                            
            except ValueError:
                fallback2standard = True

        if not fallback2standard:    
            # If we have a valid bid, use spot instances.
            try:
                float(spot_instance_bid)
                # TODO: Add support for placement groups
                
                requests = self.ec2_connection.request_spot_instances(price=spot_instance_bid,image_id=image.id,count=number_nodes, key_name=self.cloud_instance_key, user_data=None, instance_type=flavor_name, subnet_id=subnet_id, security_group_ids=security_group_ids)
            
                
                msg = "Requesting %d new %s %s spot requests from AMI %s at %s per node-hour." % (number_nodes,flavor_name,image_name,image_id,spot_instance_bid)
                print msg
                logging.info(msg)   
                time.sleep(10)     
                fulfilled_requests = [r for r in requests if r.instance_id is not None]
    
                print "Waiting up to 1 hour for spot requests"
                count = 0
                while len(fulfilled_requests) < number_nodes and count < 360:
                    time.sleep(10)
                    requests = self.ec2_connection.get_all_spot_instance_requests(request_ids=[r.id for r in requests])
                    fulfilled_requests = [r for r in requests if r.instance_id is not None]
                    count += 1
                    print "%d of %d requests filled in %d seconds" % (len(fulfilled_requests),number_nodes,count*10)
                    
                
                if count == 360:
                    print "Spot request was not fulfilled in 1 hour. Cancelling request."
                    self.ec2_connection.cancel_spot_instance_requests(request_ids=[r.id for r in requests])
                    # Should be an empty list.
                    return new_instances
                
                spot_instance_ids = [r.instance_id for r in fulfilled_requests]
                
                
                new_instances = self.ec2_connection.get_only_instances(instance_ids=spot_instance_ids)
                
    
            # If the bid is invalid, then use standard instances
            except ValueError:
                fallback2standard = True
        
        if fallback2standard:

            reservation = self.ec2_connection.run_instances(image_id=image.id,min_count=number_nodes, max_count=number_nodes, key_name=self.cloud_instance_key, user_data=None, instance_type=flavor_name, subnet_id=subnet_id, security_group_ids=security_group_ids)

            
            msg = "Creating %d new %s %s instances from AMI %s." % (number_nodes,flavor_name,image_name,image_id)
            print msg
            logging.info(msg)
    
            print "Waiting 60s for instances."
            time.sleep(60)
            
            count = 0
            while len(reservation.instances) < number_nodes and count < 24:
                print "Waiting on instances %d seconds" % count*10
                time.sleep(10)
                count +=  1
                #pprint(reservation.__dict__)
                
            new_instances = [n for n in reservation.instances]
    
        
        
        for n in new_instances:
            msg = "Created new EC2 instance %s " % n.id
            print msg
            logging.info(msg)
            #pprint(n.__dict__)
        
        return new_instances

    ##      
    # @fn associateIPAddresses(self,instances[],domain=None):	
    # Creates an new external IP address and associates	with the instances in the array.
    # @param self The object pointer
    # @param instances List of instances to associate
    # @param domain Domain on which to allocate addresses
    # @return A list of the external addresses
    #

    def associateIPAddresses(self,instances=[],domain=None):
        external_addresses = []
        try:
            all_addresses = self.ec2_connection.get_all_addresses()
            logging.info("All addresses: "+ all_addresses)
            print all_addresses
            print all_addresses[0].__dict__
        except:
            pass
        for i in instances:
            #print i.__dict__

            address = self.ec2_connection.allocate_address(domain)
            msg = "Associating ext IP %s to %s with int IP %s" % (address.public_ip,i.id,i.ip_address)
            print msg
            logging.info(msg)
            self.ec2_connection.associate_address(instance_id=i.id,public_ip=address.public_ip)
            external_addresses.append(address.public_ip)
        
            
            
        #print "Waiting 60 seconds for external networking"
        time.sleep(10)
        
        return external_addresses
        
    ##
    #
    # @fn checkCloudConnection(self):	
    # Checks to see if the EC2 connection is available.	Connects if it isn't.
    # @param self The object pointer
    #

    def checkCloudConnection(self):
        if self.ec2_connection is None:
            self.connect()

    ##
    #
    # @fn getAllEC2Instances(self):	
    # Gets all instances from EC2 connection. Returns a	list of instances.
    # @param self The object pointer
    #
    
    def getAllCloudInstances(self):
        self.checkCloudConnection()
        
        reservation_v = self.ec2_connection.get_all_instances()
        
        self.cloud_instance_list = [i for r in reservation_v for i in r.instances]
        return self.cloud_instance_list

    ##
    #
    # @fn	printAllInstanceStatus(self):	
    # Prints the status of all instances. For debugging.
    # @param self The object pointer
    #
    
    def printAllInstanceStatus(self):
        self.getAllCloudInstances()
        for instance in self.cloud_instance_list:
            print "Instance %s at %s has status %s" % (instance.id,instance.ip_address,instance.status)

        
    #
    #
    #	Future functionality
    # 
    #

    def getCloudConfigFromEnvironment(self):
        print "This should be implemented, but isn't."

    ##
    # @fn createNewCloudNodes(number_nodes,image_name,machine_type,associateip=False,domain=None):
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
    #     @param cloud_subnet cloud subnet id for primary network interface.
    #
    #    @returns list of new nodes.


    
    def createNewCloudNodes(self,number_nodes,image_name=None,flavor_name="t2.micro",local_master=None,associateip=False,domain=None,cloud_subnet=None,instance_suffix="",image_id=None,security_group_ids=None,spot_instance_bid=None):
        
        # This function creates number nodes on the cloud system. 
        # It returns a list of nodes
        
        new_instances = self.createNewCloudInstances(number_nodes,image_name,flavor_name,cloud_subnet,instance_suffix,image_id,security_group_ids,spot_instance_bid)
        # new instances should have a 60 second delay to make sure everything is running.

        ip_addresses = []
        new_ofs_test_nodes = []
        
        for idx,instance in enumerate(new_instances):
            instance.update()
            logging.info("Instance %s at %s has state %s with code %r" % (instance.id,instance.ip_address,instance.state,instance.state_code))
            
            while instance.state_code == 0:
                
                time.sleep(10)
                instance.update()
                logging.info("Instance %s at %s has state %s with code %r" % (instance.id,instance.ip_address,instance.state,instance.state_code))
            
            
        
        # now that the instances are up, check the external ip
        if associateip:
            # if we need to associate an external ip address, do so
            ip_addresses = self.associateIPAddresses(new_instances,domain)
        else:
            #otherwise use the default internal address
            
            for i in new_instances:
                i.update()
                msg = "Instance %s using Public IP: %s ; Private IP: %s" % (i.id,i.ip_address,i.private_ip_address)
                print msg
                logging.info(msg)
                #pprint(i.__dict__)
                ip_addresses.append(i.ip_address)
               

        print "===========================================================" 
        print "Adding new nodes to OFS cluster"
        
        ts = str(datetime.now()).split('.')[0]
 
        for idx,instance in enumerate(new_instances):
            # Create the node and get the instance name
            if "buntu" in image_name:
                name = 'ubuntu'
            elif "ebian" in image_name:
                name = 'debian'

            elif "edora" in image_name:
                # fedora 18 = cloud-user, fedora 19 = fedora
                
                # fedora 18 = cloud-user, fedora 19 = fedora
                name = 'fedora'
            elif "entos" in image_name or "entOS" in image_name:
                name = 'centos'
            elif "rhel7" in image_name:
                name = 'cloud-user'
            else:
                name = 'ec2-user'
            
            
        
            instance.add_tag("Name","ofsnode-%03d %s %s" % ((idx+1),ts,image_name))
            
            new_node = OFSTestRemoteNode.OFSTestRemoteNode(username=name,ip_address=instance.private_ip_address,key=self.cloud_instance_key_location,local_node=local_master,is_cloud=True,ext_ip_address=ip_addresses[idx])

            new_ofs_test_nodes.append(new_node)

        # return the list of newly created nodes.
        
        return new_ofs_test_nodes

