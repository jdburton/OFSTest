#!/usr/bin/python
##
# @class OFSTestNetwork.py
#
# OFSTestNework is the class that forms the abstraction for the cluster. All operations on the cluster
# should be performed via OFSTestNetwork, not the OFSTestNodes.
#
# Every network must have the following:
#
# 1. At least one OFSTestNode in the network_nodes array.
# 2. A local_master, which represents the local machine from which the tests are run.
#
# Cloud/OpenStack based virtual networks will also have an cloud_connection_manager.
#


import os
import OFSTestNode
import OFSTestLocalNode 
import OFSTestRemoteNode 
import Queue
import threading
import time
from pprint import pprint
import logging

class OFSTestNetwork(object):

    ##
    #
    # @fn __init__(self)
    #
    # Initializes variables and creates local master.
    #
    # @param self The object pointer
    

    def __init__(self):
    
        # Configuration for cloud 
        self.cloud_connection_manager = None
        # dictionary of instances
           
        self.network_nodes = []
        
        print "==================================================================="
        print "Checking Local machine"
        self.local_master = OFSTestLocalNode.OFSTestLocalNode()
        self.mpi_nfs_directory = ""
        self.openmpi_version = ""
        self.number_mpi_slots = 1
        self.number_mpi_hosts = 1
        self.logfile="cloudnodes.lst"

    ##
    # @fn  findNode(self,ip_address="",hostname=""):
    #
    # Finds an OFSTestNode by ip address or hostname
    #
    # @param self The object pointer
    # @param ip_address IP address of the node
    # @param hostname Hostname of the node
    #
    # @returns OFSTestNode if found, None, if not found.
    #

    def findNode(self,ip_address="",hostname=""):
    
        
        if ip_address != "":
            if ip_address == self.local_master.ip_address:
                return self.local_master
            else:
                return next((i for i in self.network_nodes if i.ip_address == ip_address), None) 
        elif hostname != "":
            logging.info("Available host names")
            logging.info([i.hostname for i in self.network_nodes])
            if hostname == self.local_master.hostname:
                return self.local_master
            else:
                return next((i for i in self.network_nodes if i.hostname == hostname), None) 
        else:
            return None

    ##
    #  @fn addRemoteNode(self,username,ip_address,key,is_cloud=False,ext_ip_address=None):
    #
    #    Creates a new OFSTestNode from an existing physical or cloud node and adds it to the network_nodes list.
    #
    # @param self The object pointer
    # @param username User login
    # @param ip_address IP address of node
    # @param key ssh key file location to access the node for username
    # @param is_cloud Is this an Cloud/OpenStack node?
    # @param ext_ip_address Externally accessible IP address
    #
    #  @returns the OFSTestNode
    #

        
    def addRemoteNode(self,username,ip_address,key,is_cloud=False,ext_ip_address=None):
        #This function adds a remote node
        
        # Is this a remote machine or existing cloud node?
        remote_node = OFSTestRemoteNode.OFSTestRemoteNode(username=username,ip_address=ip_address,key=key,local_node=self.local_master,is_cloud=is_cloud,ext_ip_address=ext_ip_address)
                
        # Add to the node dictionary
        self.network_nodes.append(remote_node)
        
        # Return the new node
        return remote_node


    ##
    #    @fn runSimultaneousCommands(self,node_list,node_function=OFSTestNode.OFSTestNode.runSingleCommand,args=[],kwargs={})
    #
    #    Runs a command on multiple nodes.
    #
    #    @param self The object pointer
    #    @param node_list  List of nodes to run command on 
    #    @param node_function Python function to run on all OFSTestNodes. Default is OFSTestNode.runSingleCommand
    #    @param args Arguments to Python node_function
    #    @param kwargs Keyword args to Python node_function
    #
        
        
    def runSimultaneousCommands(self,node_list=None,node_function=OFSTestNode.OFSTestNode.runSingleCommand,args=[],kwargs={}):
        
        #passes in a thread class that does the work on a node list with arguments args
        
        if node_list is None:
            node_list = self.network_nodes
         
        queue = Queue.Queue()
        class NodeThread(threading.Thread):

            def __init__(self, queue):
                threading.Thread.__init__(self)
                self.queue = queue
          
            def run(self):
                while True:
                    #grabs host from queue
                    #print "Queue length is %d" % self.queue.qsize()
                    node = self.queue.get()
                    
                    try:
    
                        #runs the selected node function
                        if len(args) > 0:
                            rc = node_function(node,*args)
                        elif len(kwargs) > 0:
                            rc = node_function(node,**kwargs)
                        else:
                            rc = node_function(node)
                    except:
                        logging.exception("Thread failed!");
    
                    #signals to queue job is done
                    self.queue.task_done()
          
          
        start = time.time()
          
          
        #spawn a pool of threads, and pass them queue instance 
        #pool of threads will be the same number as the node list
        for n in node_list:
            t = NodeThread(queue)
            t.setDaemon(True)
            t.start()
              
        #populate queue with data   
        for node in node_list:
            queue.put(node)
           
        #wait on the queue until everything has been processed     
        queue.join()
          

    ##
    # @fn   addCloudConnection(self,cloud_config_file,key_name,key_location)
    #
    #    Initialize the CloudConnection
    #
    #    @param self The object pointer
    #    @param cloud_config_file location of cloudrc.sh file 
    #    @param key_name Name of Cloud key to access node
    #    @param key_location Location of .pem file that contains the Cloud key
    #
   
    
    
    def addCloudConnection(self,cloud_config_file,key_name,key_location,cloud_type="EC2",nova_password_file=None,region_name=None):
        
        import OFSCloudConnectionManager
        
        #This function initializes the cloud connection
        self.cloud_type = cloud_type
        if (cloud_type == 'EC2'):
            import OFSEC2ConnectionManager
            self.cloud_connection_manager = OFSEC2ConnectionManager.OFSEC2ConnectionManager(cloud_config_file,region_name)
        elif (cloud_type == 'nova'):
            import OFSNovaConnectionManager
            self.cloud_connection_manager = OFSNovaConnectionManager.OFSNovaConnectionManager(cloud_config_file,password_file=nova_password_file)
        self.cloud_connection_manager.setCloudKey(key_name,key_location)
        

    ##
    # @fn createNewCloudNodes(number_nodes,image_name,machine_type,associateip=False,domain=None,cloud_subnet=None,instance_suffix="",image_id=None,security_group_ids=None,spot_instance_bid=None):
    #
    # Creates new cloud nodes and adds them to network_nodes list.
    #
    #
    #    @param self The object pointer  
    #    @param number_nodes  number of nodes to be created
    #    @param image_name  Name of Cloud image to launch
    #    @param machine_type  Cloud "flavor" of virtual node
    #    @param associateip  Associate to external ip?
    #    @param domain Domain to associate with external ip
    #	 @param cloud_subnet cloud subnet id for primary network interface.
    #    @param instance_suffix
    #    @param instance_id ID of instance to be launched.
    #    @param security_group_ids List of security group ids for this instance.
    #    @param spot_instance_bid Maximum bid for spot instances. Ignored if not applicable.
    #
    #    @returns list of new nodes.


    
    def createNewCloudNodes(self,number_nodes,image_name=None,machine_type="t2.micro",associateip=False,domain=None,cloud_subnet=None,instance_suffix="",image_id=None,security_group_ids=None,spot_instance_bid=None):
        
        # This function creates number nodes on the cloud system. 
        # It returns a list of nodes
        new_ofs_test_nodes = self.cloud_connection_manager.createNewCloudNodes(number_nodes,image_name,machine_type,self.local_master,associateip,domain,cloud_subnet,instance_suffix,image_id,security_group_ids,spot_instance_bid)
        
        self.logNewCloudNodes(new_ofs_test_nodes)
                
        # Add the node to the created nodes list.
        for new_node in new_ofs_test_nodes:
            self.network_nodes.append(new_node)
        
        # return the list of newly created nodes.
        
        rc = self.checkExternalConnectivity()
        count = 0
        while rc != 0 and count < 300:
            count += 10
            print "Waiting %ds of 300s for connectivity to new nodes" % count 
            time.sleep(10)
            rc = self.checkExternalConnectivity()
            
            
        
        return new_ofs_test_nodes
    
    
    def logNewCloudNodes(self,new_ofs_test_nodes):
        
        output = open(self.logfile,"w")
        for node in new_ofs_test_nodes:
            output.write(node.ip_address+"\n")
        output.close()
    

##
# @fn uploadKeys(node_list=None)
#
# Upload ssh keys to the list of remote nodes
#
#    @param self The object pointer
#    @param node_list list of nodes to upload the keys.
#

 

    def uploadKeys(self,node_list=None):
        # if a list is not provided upload all keys
        if node_list is None:
            node_list = self.network_nodes
            
        for node in node_list:
            self.runSimultaneousCommands(node_list=node_list,node_function=OFSTestRemoteNode.OFSTestRemoteNode.uploadRemoteKeyFromLocal, args=[self.local_master,node.ext_ip_address])
        

    ##      
    # @fn enablePasswordlessSSH(self,node_list=None):
    #
    # Enable passwordless SSH for the node for the current user.
    #
    #    @param self The object pointer
    #    @param node_list List of nodes to enable passwordless ssh
            

    def enablePasswordlessSSH(self,node_list=None,user=None):
        
        if node_list is None:
            node_list = self.network_nodes
        

        
        for src_node in node_list:
            
            if user is None:
                user = src_node.current_user
        
            if user == "root":
                home_dir = "/root"
            else:
                home_dir = "/home/"+user
            
            # passwordless access to localhost
            src_node.runSingleCommand("/usr/bin/ssh-keyscan localhost >> %s/.ssh/known_hosts" % home_dir)
            src_node.runSingleCommand("/usr/bin/ssh-keyscan 127.0.0.1 >> %s/.ssh/known_hosts" % home_dir)
            
            for dest_node in node_list:
                # passwordless access to all other nodes
                logging.info("Enabling passwordless SSH from %s to %s/%s/%s" % (src_node.hostname,dest_node.hostname,dest_node.ip_address,dest_node.ext_ip_address))
                src_node.runSingleCommand("/usr/bin/ssh-keyscan %s >> %s/.ssh/known_hosts" % (dest_node.hostname,home_dir))
                src_node.runSingleCommand("/usr/bin/ssh-keyscan %s >> %s/.ssh/known_hosts" % (dest_node.ext_ip_address,home_dir))
                src_node.runSingleCommand("/usr/bin/ssh-keyscan %s >> %s/.ssh/known_hosts" % (dest_node.ip_address,home_dir))
                

    ##      
    # @fn terminateCloudNode(self, remote_node)
    #
    # Terminate the remote node and remove it from the created node list.
    #
    #    @param self The object pointer
    #    @param remote_node Node to be terminated.


    def terminateCloudNode(self,remote_node):
                
        if remote_node.is_cloud == False: 
            logging.exception("Node at %s is not controlled by the cloud manager." % remote_node.ip_address)
            return
        
        failures = 0
        rc = self.terminateCloudInstance(remote_node.ip_address)
        
        # if the node was terminated, remove it from the list.
        if rc == 0:
            self.network_nodes = [ x for x in self.network_nodes if x.ip_address != remote_node.ip_address]
        else:
            logging.exception( "Could not delete node at %s, error code %d" % (remote_node.ip_address,rc))
            failures += 1
            
        return failures
    
    ##      
    # @fn terminateCloudInstance(self, remote_node)
    #
    # Terminate the remote instance associated with the ip_address
    #
    #    @param self The object pointer
    #    @param ip_address of instance to be terminated.


    def terminateCloudInstance(self,ip_address):
        
        rc = self.cloud_connection_manager.terminateCloudInstance(ip_address)
                
 
        return rc

    ##      
    # @fn terminateAllInstancesFromList(self, logfile)
    #
    # Terminate all the instances in a given logfile.
    #
    #    @param self The object pointer
    #    @param logfile Logfile that contains a list of instance IP addresses.
    
    
    def terminateAllInstancesFromList(self, logfile=None):
        if logfile is None:
            logfile = self.logfile
        list = self.getInstanceList(logfile)
        
        if list is None:
            return 0
        
        errors = 0
        for ip_address in list:
            rc = self.terminateCloudInstance(ip_address)
            if rc != 0:
                logging.exception("Could not terminate instance at %s" % ip_address)
                errors += 1

        return errors

    ##      
    # @fn stopCloudNode(self, remote_node)
    #
    # Stop the remote node and remove it from the created node list.
    #
    #    @param self The object pointer
    #    @param remote_node Node to be terminated.


    def stopCloudNode(self,remote_node):
                
        if remote_node.is_cloud == False: 
            logging.exception("Node at %s is not controlled by the cloud manager." % remote_node.ip_address)
            return
        
        rc = self.cloud_connection_manager.stopCloudInstance(remote_node.ip_address)
        
        # if the node was terminated, remove it from the list.
        if rc == 0:
            self.network_nodes = [ x for x in self.network_nodes if x.ip_address != remote_node.ip_address]
        else:
            logging.exception( "Could not delete node at %s, error code %d" % (remote_node.ip_address,rc))
            
        return rc

    ##      
    # @fn updateCloudNodes(self,node_list=None, custom_kernel=False, kernel_git_location=None, kernel_git_branch=None,host_prefix="ofsnode"):
    #
    #    Update only the Cloud Nodes
    # 
    # @param self The object pointer
    # @param node_list List of nodes to update.
    # @param custom_kernel Build a custom linux kernel?
    # @param kernel_git_location url of git repository from which the custom kernel will be built.
    # @param kernel_git_branch url of git branch from which the custom kernel will be built.
    # @param host_prefix prefix of the hostname of the created nodes.
    

        
    def updateCloudNodes(self,node_list=None, custom_kernel=False, kernel_git_location=None, kernel_git_branch=None,host_prefix="ofsnode"):
        # This only updates the Cloud controlled nodes
         
        if node_list is None:
            node_list = self.network_nodes
        
        cloud_nodes = [node for node in self.network_nodes if node.is_cloud == True]
        return self.updateNodes(cloud_nodes,custom_kernel,kernel_git_location,kernel_git_branch,host_prefix)   


    ##
    # @fn updateEtcHosts(self,node_list=None):
    #
    # This function updates the etc hosts file on each node with the hostname and ip
    # address. Also creates the necessary mpihosts config files.
    #
    #    @param self The object pointer
    #    @param node_list List of nodes in network


    def updateEtcHosts(self,node_list=None):
        
        #This function updates the etc hosts file on each node with the 
        if node_list is None:
            node_list = self.network_nodes
        
        
        self.number_mpi_hosts = len(node_list) 

        self.number_mpi_slots = 0
        
        for node in node_list:
            node.number_mpi_slots = 0
            node.number_mpi_hosts = self.number_mpi_hosts
            node.created_openmpihosts = "/home/%s/openmpihosts" % node.current_user
            node.created_mpichhosts = "/home/%s/mpichhosts" % node.current_user
            for n2 in node_list:
                # limit slots to 4 per node.
                mpi_slots = 4
                if n2.number_cores < 4:
                    mpi_slots = n2.number_cores
                    
                node.number_mpi_slots += mpi_slots
                # can we ping the node?
                #print "Pinging %s from local node" % n2.hostname
                rc = node.runSingleCommandAsRoot("ping -c 1 %s" % n2.hostname)
                # if not, add to the /etc/hosts file
                if rc != 0:
                    logging.info("Could not ping %s at %s from %s. Manually adding to /etc/hosts" % (n2.hostname,n2.ip_address,node.hostname))
                node.runSingleCommandAsRoot('bash -c \'echo -e "%s     %s     %s" >> /etc/hosts\'' % (n2.ip_address,n2.hostname,n2.hostname))
                # also create mpihosts files while we're here.
                node.runSingleCommand('echo "%s   slots=%d" >> %s' % (n2.hostname,mpi_slots,node.created_openmpihosts))
                node.runSingleCommand('echo "%s:%d" >> %s' % (n2.hostname,mpi_slots,node.created_mpichhosts))
            
            
            self.number_mpi_slots = node.number_mpi_slots
                    
            node.hostname = node.runSingleCommandBacktick("hostname")

    ##
    # @fn updateNodes(self,node_list, custom_kernel=False, kernel_git_location=None, kernel_git_branch=None,host_prefix="ofsnode")
    #
    # This updates the system software on the list of nodes.
    #
    #    @param self The object pointer
    #    @param node_list List of nodes to update
    #    @param custom_kernel Build a custom linux kernel?
    #    @param kernel_git_location url of git repository from which the custom kernel will be built.
    #    @param kernel_git_branch url of git branch from which the custom kernel will be built.
    #    @param host_prefix prefix of the hostname of the created nodes.
     
    def updateNodes(self,node_list=None, custom_kernel=False, kernel_git_location=None, kernel_git_branch=None,host_prefix="ofsnode"):
        if node_list is None:
            node_list = self.network_nodes
            
        # Run updateNode on the nodes simultaneously. 
        self.runSimultaneousCommands(node_list=node_list,node_function=OFSTestNode.OFSTestNode.updateNode,args=[custom_kernel,kernel_git_location,kernel_git_branch])
        # Wait for reboot
        print "Waiting 180s for nodes to reboot"
        time.sleep(180)
        
        rc = self.checkExternalConnectivity()
        count = 0
        while rc != 0 and count < 300:
            count += 10
            print "Waiting %ds of 300s for connectivity to new nodes" % count 
            time.sleep(10)
            rc = self.checkExternalConnectivity()
        
        if rc != 0:
            return rc
        
        print "Nodes rebooted."
        # workaround for strange cuer1 issue where hostname changes on reboot.
        for node in node_list:
            # node information may have changed during reboot.
            old_hostname = node.hostname
            node.currentNodeInformation(host_prefix)
            tmp_hostname = node.runSingleCommandBacktick("hostname")
            if tmp_hostname != old_hostname:
                logging.info( "Hostname changed from %s to %s! Resetting to %s" % (old_hostname,tmp_hostname,old_hostname))
                node.runSingleCommandAsRoot("hostname %s" % old_hostname)
        
        return 0
    
    ##
    # @fn installRequiredSoftware(self,node_list=None):
    #
    # This installs the required software on all the nodes simultaneously.
    #
    #    @param self The object pointer
    #    @param node_list List of nodes to update
                    
        
    
    def installRequiredSoftware(self,node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        self.runSimultaneousCommands(node_list=node_list,node_function=OFSTestNode.OFSTestNode.installRequiredSoftware)
        
        
    ##
    # @fn installDB4(self,node_list=None):
    #
    # This installs the required software on all the nodes
    #
    #    @param self The object pointer
    #    @param node_list List of nodes to update
                    
        
    
    def installDB4(self,node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        self.runSimultaneousCommands(node_list=node_list,node_function=OFSTestNode.OFSTestNode.installDB4)

    ##
    # @fn installHadoop(self,hadoop_version,node_list=None):
    #
    # This installs the required software on all the nodes
    #
    #    @param self The object pointer
    #    @param hadoop_version Version of hadoop to install
    #    @param node_list List of nodes to update
                    
        
    
    def installHadoop(self,hadoop_version="hadoop-1.2.1",node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        for node in node_list:
            node.hadoop_version=hadoop_version
            
        self.runSimultaneousCommands(node_list=node_list,node_function=OFSTestNode.OFSTestNode.installHadoop)
    
    ##
    # @fn buildOFSFromSource(
    #         resource_type,
    #         resource_location,
    #         download_location=None,
    #         build_node=None,
    #         build_kmod=True,
    #         enable_strict=False,
    #         enable_fuse=False,
    #         enable_shared=False,
    #         enable_hadoop=False,
    #         ofs_prefix="/opt/orangefs",
    #         db4_prefix="/opt/db4",
    #         security_mode=None,
    #         ofs_patch_files=[],
    #         configure_opts="",
    #         make_opts="",
    #         debug=False,
    #         node_list=None,        
    #         hadoop_version="hadoop-2.6.0",
    #         ofs_database="lmdb",
    #         svn_username="",
    #         svn_password=""):
    #
    #
    # This builds OrangeFS on the build node
    #
    #    @param self The object pointer
    #    @param resource_type What form is the source tree? (SVN,TAR,LOCAL) etc.
    #    @param resource_location Where is the source located?
    #    @param download_location Where should the source be downloaded to?
    #    @param build_node    On which node should OFS be build (default first)
    #    @param build_kmod    Build kernel module
    #    @param enable_strict    Enable strict option
    #    @param enable_fuse    Build fuse module
    #    @param enable_shared     Build shared libraries
    #    @param enable_hadoop    Build hadoop support
    #    @param ofs_prefix    Where should OFS be installed?
    #    @param db4_prefix    Where is db4 located?
    #    @param security_mode    None, Cert, Key
    #    @param ofs_patch_files Location of OrangeFS patches.
    #    @param configure_opts    Additional configure options
    #    @param make_opts        Make options
    #    @param debug    Enable debugging
    #    @param svn_options    Additional options for SVN
    #    @param node_list List of nodes to update
    #    @param hadoop_version Version of hadoop use 
    #    @param ofs_database Database for metadata storage (bdb or lmdb)
    #    @param svn_username Username to use to log in to svn
    #    @param svn_password Password to use to log into svn
    
          

    def buildOFSFromSource(self,
        resource_type,
        resource_location,
        download_location=None,
        build_node=None,
        build_kmod=True,
        enable_strict=False,
        enable_fuse=False,
        enable_shared=False,
        enable_hadoop=False,
        ofs_prefix="/opt/orangefs",
        db4_prefix="/opt/db4",
        security_mode=None,
        ofs_patch_files=[],
        configure_opts="",
        make_opts="",
        debug=False,
        svn_options=None,
        node_list=None,
        hadoop_version="hadoop-2.6.0",
        ofs_database="lmdb",
        svn_username="",
        svn_password=""
        ):
        
        output = []
        dir_list = ""
        
        msg = "Resource type is "+resource_type+" location is "+resource_location
        print msg
        logging.info(msg)
        
        if node_list is None:
            node_list = self.network_nodes
        
        if build_node is None:
            build_node = node_list[0]
            
        if download_location is None:
            download_location = "/home/%s/" % build_node.current_user
        
        if resource_type == "LOCAL":
            # copy from the local to the buildnode, then pretend it is a "buildnode" resource.
            # shameless hack.
            #print "Local resource"
            # get the basename from the resource location
            dir_list = os.path.basename(resource_location)
            #print dir_list
            # add the directory to the download location
            #download_location = "%s%s" % (download_location,dir_list)
            # create the destination directory
            #rc = build_node.runSingleCommand("mkdir -p "+download_location)
            #print "Copying source from %s to %s" % (resource_location,build_node.hostname)
            rc = self.local_master.copyToRemoteNode(resource_location,build_node,download_location,True)
            if rc != 0:
                logging.exception("Could not copy source from %s to %s" % (resource_location,build_node.hostname))
                return rc
            #rc = build_node.runSingleCommand("ls -l "+download_location+dir_list,output)
            #print output
            
            #print "Calling build_node.copyOFSSource(%s,%s,%s)" %(resource_type,resource_location,download_location+dir_list)
        
            resource_type = "BUILDNODE"
            resource_location = download_location+dir_list
            
        rc = build_node.copyOFSSource(resource_type=resource_type,resource=resource_location,dest_dir=download_location+dir_list,options=svn_options,username=svn_username,password=svn_password)
        
        if rc != 0:
            return rc

        for patch in ofs_patch_files:
            
            patch_name = os.path.basename(patch)
            rc = self.local_master.copyToRemoteNode(patch,build_node,"%s/%s" % (build_node.ofs_source_location,patch_name),False)
            if rc != 0:
                logging.exception("Could not upload patch at %s to buildnode %s" % (patch,build_node.hostname))
                return rc


        rc = build_node.configureOFSSource(build_kmod=build_kmod,enable_strict=enable_strict,enable_shared=enable_shared,enable_fuse=enable_fuse,ofs_prefix=ofs_prefix,db4_prefix=db4_prefix,ofs_patch_files=ofs_patch_files,configure_opts=configure_opts,security_mode=security_mode,enable_hadoop=enable_hadoop,hadoop_version=hadoop_version,ofs_database=ofs_database)
        if rc != 0:
            return rc
        
        rc = build_node.makeOFSSource(make_opts)
        if rc != 0:
            return rc
        
        return rc

   
    ##    
    #    @fn installOFSBuild(self,build_node=None,install_opts="",node_list=None):
    #
    #    Install the OrangeFS build on a given node
    #    @param self The object pointer
    #    @param build_node Node on which to build OrangeFS
    #    @param install_opts Other install options
    #    @param node_list List of nodes in network
           
        
    def installOFSBuild(self,build_node=None,install_opts="",node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        
        if build_node is None:
            build_node = self.network_nodes[0]
        return build_node.installOFSSource(install_opts)
    
   
    ##    
    #    @fn installOFSTests(self,build_node=None,install_opts=""):
    #
    #    Install the OrangeFS tests in the source code on a given node
    #    @param self The object pointer
    #    @param client_node Node on which to install OrangeFS tests
    #    @param configure_opts Other install options
    #    @param node_list List of nodes in network.
 

    def installOFSTests(self,client_node=None,configure_options="",node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        if client_node is None:
            client_node = node_list[0]
        return client_node.installOFSTests(configure_options)

   
    ##    
    #    @fn installBenchmarks(self,build_node=None,node_list=None):
    #
    #    Install the 3rd party benchmarks on the given node.
    #    @param self The object pointer
    #    @param build_node Node on which to install benchmark tests
    #    @param node_list List of nodes in network.
 

    def installBenchmarks(self,build_node=None,node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        if build_node is None:
            build_node = node_list[0]
        return build_node.installBenchmarks("%s/benchmarks-20121017.tar.gz" % build_node.url_base,"/home/%s/benchmarks" % build_node.current_user)

   
    ##    
    #    @fn configureOFSServer(self,ofs_fs_name,master_node=None,node_list=None,pvfs2genconfig_opts="",security=None,number_metadata_servers=1,dedicated_client=False,servers_per_node=1,number_data_servers=None):
    #
    #    @param self The object pointer
    #    @param ofs_fs_name    Default name of OrangeFS service: version < 2.9 = "pvfs2-fs"; version >= 2.9 = "orangefs"
    #    @param master_node    Master node in the cluster.
    #    @param node_list      List of nodes in OrangeFS cluster
    #    @param pvfs2genconfig_opts = Additional options for pvfs2genconfig utility
    #    @param security        None, "Key", "Cert"
    #    @param number_metadata_servers Number of metadata servers on the network
    #    @param dedicated_client Test on a dedicated client
    #    @param servers_per_node Number of servers per node
    #    @param number_data_servers Number of data servers on the network.)

 
       
    def configureOFSServer(self,ofs_fs_name,master_node=None,node_list=None,ofs_data_location="",ofs_metadata_location="",pvfs2genconfig_opts="",security=None,number_metadata_servers=1,dedicated_client=False,servers_per_node=1,number_data_servers=None):
        if node_list is None:
            node_list = self.network_nodes
        if master_node is None:
            master_node = node_list[0]
        return master_node.configureOFSServer(ofs_hosts_v=node_list,ofs_fs_name=ofs_fs_name,ofs_data_location=ofs_data_location,ofs_metadata_location=ofs_metadata_location,configuration_options=pvfs2genconfig_opts,security=security,number_metadata_servers=number_metadata_servers,dedicated_client=dedicated_client,servers_per_node=servers_per_node,number_data_servers=number_data_servers)

   
    ##    
    #    @fn copyOFSToNodeList(self,destination_list=None):
    #
    #    Copy OFS from build node to rest of cluster.
    #    
    #    @param self The object pointer
    #    @param destination_list List of nodes to copy OrangeFS to. OFS should already be at destination_list[0].
        
    def copyOFSToNodeList(self,destination_list=None):
        if destination_list is None:
            destination_list = self.network_nodes;
        self.copyResourceToNodeList(node_function=OFSTestNode.OFSTestNode.copyOFSInstallationToNode,destination_list=destination_list)




    ##    
    #    @fn copyOpenMPIToNodeList(self,destination_list=None):
    #
    #    Copy OpenMPI from build node to rest of cluster.
    #    
    #    @param self The object pointer
    #    @param destination_list List of nodes to copy OrangeFS to. OFS should already be at destination_list[0].
        
    def copyOpenMPIToNodeList(self,destination_list=None):
        if destination_list is None:
            destination_list = self.network_nodes;
        self.copyResourceToNodeList(node_function=OFSTestNode.OFSTestNode.copyOpenMPIInstallationToNode,destination_list=destination_list)


    ##    
    #  @fn copyResourceToNodeList(self,node_function,destination_list=None):
    #
    # This is a multi-threaded recursive copy routine.
    # Function copies OrangeFS from list[0] to list[len/2]
    # Then it partitions the list into two parts and copies again. This copies at
    # O(log n) time.
    #
    # For an eight node setup [0:7], copy is as follows:
    # 1: 0->4
    # 2: 0->2 4->6
    # 3: 0->1 2->3 4->5 6->7
    #
    #    @param self The object pointer
    #    @param node_function    Python function/method that does copying
    #    @param destination_list    list of nodes. Assumption is source is at node[0].
        

    def copyResourceToNodeList(self,node_function,destination_list=None, *args, **kwargs):

        
        if destination_list is None:
            destination_list = self.network_nodes
            
        # This assumes that the OFS installation is at the destination_list[0]
        list_length = len(destination_list)
        
        # If our list is of length 1 or less, return.
        if list_length <= 1:
            return 
        
        #copy from list[0] to list[list_length/2]
        msg = "Copying from %s to %s" % (destination_list[0].ip_address,destination_list[list_length/2].ip_address)
        print msg
        logging.info(msg)
        #rc = destination_list[0].copyOFSInstallationToNode(destination_list[list_length/2])
        rc = node_function(destination_list[0],destination_list[list_length/2], *args, **kwargs)
        
        
        # TODO: Throw an exception if the copy fails.
       
        queue = Queue.Queue()
        class CopyThread(threading.Thread):

            def __init__(self, queue,manager):
                threading.Thread.__init__(self)
                self.queue = queue
                self.manager = manager
          
            def run(self):
                while True:
                    #grabs host from queue
                    #print "Queue length is %d" % self.queue.qsize()
                    list = self.queue.get()
                    try:
                    
                        #print "Copying %r" % list
                        self.manager.copyResourceToNodeList(node_function=node_function,destination_list=list, *args, **kwargs)
                    except:
                        logging.exception("Copy failed!")
                        
                    #signals to queue job is done
                    self.queue.task_done()
          
          
        start = time.time()
          
          
        #spawn two threads to partition the list.
        for n in range(2):
            t = CopyThread(queue,self)
            t.setDaemon(True)
            t.start()
              
        #populate queue with data   
        queue.put(destination_list[:list_length/2])
        queue.put(destination_list[list_length/2:])
           
        #wait on the queue until everything has been processed     
        queue.join()
    
   
    ##    
    #    @fn stopOFSServers(self,node_list=None):
    #
    #    Stops the OrangeFS servers on the nodes
    #    @param self The object pointer
    #    @param node_list List of nodes in network.
     
          
    def stopOFSServers(self,node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        self.runSimultaneousCommands(node_list=node_list,node_function=OFSTestNode.OFSTestNode.stopOFSServer)
        time.sleep(20)

   
    ##    
    #    @fn startOFSServers(self,node_list=None):
    #
    #    Starts the OrangeFS servers on the nodes
    #
    #    @param self The object pointer
    #    @param node_list List of nodes in network.
     

    def startOFSServers(self,node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        self.runSimultaneousCommands(node_list=node_list,node_function=OFSTestNode.OFSTestNode.startOFSServer)
        time.sleep(20)

   
    ##    
    #    @fn startOFSClientAllNodes(self,security=None,disable_acache=False):
    #
    #    Starts the OrangeFS servers on all created nodes
    #    @param self The object pointer
    #    @param security OFS security mode: None,"Key","Cert"
    #    @param node_list List of nodes in network.
    #    @param disable_acache Disable the acache
     

    def startOFSClientAllNodes(self,security=None,node_list=None,disable_acache=False):
        if node_list is None:
            node_list = self.network_nodes
        for node in node_list:
            self.startOFSClient(client_node=node,security=security,disable_acache=disable_acache)
   
    ##    
    #    @fn startOFSClient(self,client_node=None,security=None,disable_acache=False):
    #
    #    Starts the OrangeFS servers on one node
    #
    #    @param self The object pointer
    #    @param client_node Node on which to run OrangeFS client
    #    @param security OFS security mode: None,"Key","Cert"
    #    @param node_list List of nodes in network.
    #    @param disable_acache Disable the acache
            
    def startOFSClient(self,client_node=None,security=None,node_list=None,disable_acache=False):
        if node_list is None:
            node_list = self.network_nodes
        if client_node is None:
            client_node = node_list[0]
        client_node.installKernelModule()
        #client_node.runSingleCommand('/sbin/lsmod | grep pvfs')
        client_node.startOFSClient(security=security,disable_acache=disable_acache)


        time.sleep(10)
        #client_node.runSingleCommand('ps aux | grep pvfs')

    ##
    # @fn mountOFSFilesystem(self,mount_fuse=False,client_node=None,node_list=None):
    #    Mount OrangeFS on a given client node.
    #    @param self The object pointer
    #    @param mount_fuse Mount using fuse module?
    #    @param client_node Node on which to run OrangeFS client
    #    @param node_list List of nodes in network.


    def mountOFSFilesystem(self,mount_fuse=False,client_node=None,node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        if client_node is None:
            client_node = node_list[0]
        client_node.mountOFSFilesystem(mount_fuse=mount_fuse)
        time.sleep(10)
        print "Checking mount"
        mount_res=client_node.runSingleCommandBacktick("mount | grep -i pvfs")
        print mount_res
        logging.info("Checking Mount: "+mount_res)

   
    ##    
    # @fn mountOFSFilesystemAllNodes(self,mount_fuse=False,node_list=None):
    #
    #    Mount OrangeFS on all nodes
    #    @param self The object pointer
    #    @param mount_fuse Mount using fuse module?
    #    @param node_list List of nodes in network.


    def mountOFSFilesystemAllNodes(self,mount_fuse=False,node_list=None):
        
        # TODO: make this multithreaded
        for node in self.network_nodes:
            self.mountOFSFilesystem(mount_fuse=mount_fuse,client_node=node)
   
    ##    
    #    @fn stopOFSClient(self,client_node=None,node_list=None):
    #
    #    Stop the OrangeFS client on a given node
    #    @param self The object pointer
    #    @param client_node Node on which to run OrangeFS client
    #    @param node_list List of nodes in network.


        
    def stopOFSClient(self,client_node=None,node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        if client_node is None:
            client_node = node_list[0]
        client_node.stopOFSClient()
        
   
    ##    
    #    @fn stopOFSClientAllNodes(self,node_list=None):
    #
    #    Stop the OrangeFS client on all nodes in list
    #    @param self The object pointer
    #    @param node_list List of nodes in network.



    def stopOFSClientAllNodes(self,node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        # TODO: make this multithreaded
        for node in node_list:
            self.stopOFSClient(node)

   
    ##    
    #    @fn unmountOFSFilesystemAllNodes(self,node_list=None):
    #
    #    Unmount the OrangeFS directory on all nodes in list    
    #    @param self The object pointer
    #    @param node_list List of nodes in network.



    
    def unmountOFSFilesystemAllNodes(self,node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        # TODO: make this multithreaded
        for node in node_list:
            node.unmountOFSFilesystem()

   
    ##    
    #    @fn terminateAllCloudNodes(self,node_list=None):
    #
    #    Terminate all the cloud nodes in a list
    #    @param self The object pointer
    #    @param node_list List of nodes in network.



    def terminateAllCloudNodes(self, node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        rc = 0
        for node in node_list:
            if node.is_cloud == True:
                rc += self.terminateCloudNode(node)
        if rc == 0:
            if os.path.exists(self.logfile):
                os.remove(self.logfile)
   
       ##    
    #    @fn stopAllCloudNodes(self,node_list=None):
    #
    #    Terminate all the cloud nodes in a list
    #    @param self The object pointer
    #    @param node_list List of nodes in network.



    def stopAllCloudNodes(self, node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        for node in node_list:
            if node.is_cloud == True:
                self.stopCloudNode(node)

   
   
    ##    
    #    @fn setUrlBase(self,url_base="localhost",node_list=None):
    #
    #    Stops the OrangeFS servers on the nodes
    #    @param self The object pointer
    #    @param node_list List of nodes in network.
     
          
    def setUrlBase(self,url_base="http://localhost",node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        self.url_base = url_base
        for node in node_list:
            node.url_base = url_base

    

   
    ##    
    #   @fn generateOFSKeys(self,node_list=None,head_node=None):
    #
    #    Generate SSH keys for OrangeFS security
    #    @param self The object pointer
    #    @param node_list List of nodes in network.
    #    @param head_node Head node of ssh setup

   
    
    def generateOFSKeys(self,node_list=None,head_node=None):
        if node_list is None:
            node_list = self.network_nodes
        if head_node is None:
            head_node = node_list[0]
            
        rc = self.generateOFSServerKeys(node_list,head_node)
        if rc != 0:
            return rc
        rc = self.generateOFSClientKeys(node_list,head_node)
        if rc != 0:
            return rc
        rc = self.generateOFSKeystoreFile(node_list,head_node)
        if rc != 0:
            return rc
        return 0

   
    ##    
    #   @fn generateOFSCertificates(self,ldap_server_uri,ldap_admin,ldap_admin_password,ldap_container,node_list=None,security_node=None,):
    #
    #    Generate SSH certificates for OrangeFS cert-based security
    #    @param self The object pointer
    #    @param ldap_server_uri The uri of the LDAP server
    #    @param ldap_admin_password The password for the LDAP admin account
    #    @param ldap_container The LDAP container that contains the users for which the certificates will be generated.
    #    @param node_list List of nodes in network.
    #    @param security_node Node where the certificates are created.

   
    
    def generateOFSCertificates(self,ldap_server_uri,ldap_admin,ldap_admin_password,ldap_container,node_list=None,security_node=None,):
        if node_list is None:
            node_list = self.network_nodes
        if security_node is None:
            security_node = node_list[0]
        
        print "generateOFSCertificates(ldap_server_uri = %s, ldap_admin = %s, ldap_admin_password = %s, ldap_container = %s)" % (ldap_server_uri,ldap_admin,ldap_admin_password,ldap_container)
        
        # Do we need to setup ldap? 
        if ldap_server_uri is None or ldap_admin is None or ldap_admin_password is None or ldap_container is None:
            rc = security_node.setupLDAP()
        else:
            # if not, use current configuration.
            security_node.setLDAPConfig(ldap_server_uri,ldap_admin,ldap_admin_password,ldap_container)
            rc = 0
            
        if rc == 0:
            rc = security_node.createCACert()
            # CA Certs should be copied with OrangeFS.
        
            self.createUserCerts(node_list=node_list,security_node=security_node)
            self.createUserCerts(user="nobody",node_list=node_list,security_node=security_node)
            self.createUserCerts(user="daemon",node_list=node_list,security_node=security_node)
            self.createUserCerts(user="bin",node_list=node_list,security_node=security_node)
            self.createUserCerts(user="root",node_list=node_list,security_node=security_node)

        return rc

    ##
    #    def createUserCerts(self,user=None,node_list=None,security_node=None): 
    #    
    #    Create certificates for a given user
    #
    #    @param self The object pointer
    #    @param user User for which certificates will be generated
    #    @param security_node Node on which the certificates will be generated.
    #
    
    def createUserCerts(self,user=None,node_list=None,security_node=None):
        if node_list is None:
            node_list = self.network_nodes
        if security_node is None:
            security_node = node_list[0]
        if user is None:
            user = security_node.current_user

            
        rc = security_node.createUserCerts(user);
        if rc == 0:
            self.updateCertsUsers(user=user,destination_list=node_list)
            self.copyUserCertsToNodeList(user=user,destination_list=node_list) 
            
        
    
    ##    
    #    @fn copyUserCertsToNodeList(self,destination_list=None):
    #
    #    Copy OFS from build node to rest of cluster.
    #    
    #    @param self The object pointer
    #    @param destination_list List of nodes to copy OrangeFS to. OFS should already be at destination_list[0].
        
    def copyUserCertsToNodeList(self,user,destination_list=None):
        if destination_list is None:
            destination_list = self.network_nodes;
        self.copyResourceToNodeList(node_function=OFSTestNode.OFSTestNode.copyUserCertsToNode, destination_list=destination_list, user=user )

    ##    
    #    @fn updateCertsUsers(self,destination_list=None):
    #
    #    Update users so they are compatible with certs mode.
    #    
    #    @param self The object pointer
    #    @param destination_list List of nodes to copy OrangeFS to. OFS should already be at destination_list[0].
        
    def updateCertsUsers(self,user,destination_list=None):
        if destination_list is None:
            destination_list = self.network_nodes;
        for node in destination_list:
            node.runSingleCommandAsRoot('usermod -d /home/%s -s /bin/bash %s' % (user,user ))
            node.runSingleCommandAsRoot('mkdir -p /home/%s ' % user)
            

    ##    
    #    @fn generateOFSServerKeys(self,node_list=None,security_node=None)
    #
    #    Generate server SSH keys for OrangeFS security
    #    @param self The object pointer
    #    @param node_list List of nodes in network.
    #    @param security_node Node that generates server keys
    
    
    def generateOFSServerKeys(self,node_list=None,security_node=None):
        if node_list is None:
            node_list = self.network_nodes
        if security_node is None:
            security_node = node_list[0]
        
        #for each server, create a private server key at <orangefs>/etc/orangefs-serverkey.pem
        #cd /tmp/$USER/keys
        #openssl genrsa -out orangefs-serverkey-(remote hostname).pem 2048
        #copy  orangefs-serverkey-(remote_hostname).pem <orangefs>/etc/
        output = []
       
        
        security_node.runSingleCommand("mkdir -p /tmp/%s/security" % security_node.current_user)
        security_node.changeDirectory("/tmp/%s/security" % security_node.current_user)
        
        for node in self.network_nodes:
            keyname = "orangefs-serverkey-%s.pem" % node.hostname
            rc = security_node.runSingleCommand("openssl genrsa -out %s 2048" % keyname,output)
            if rc != 0:
                logging.exception("Could not create server security key for "+node.hostname)
                logging.exception(output) 
                return rc
            rc = security_node.copyToRemoteNode(source="/tmp/%s/security/%s" % (security_node.current_user,keyname), destination_node=node, destination="%s/etc/orangefs-serverkey.pem" % node.ofs_installation_location, recursive=False)
            if rc != 0:
                logging.exception("Could not copy server security key %s for %s " % (keyname,node.hostname))
                return rc
            
            
            #rc = node.runSingleCommand("chown 
        


        return 0

   
    ##    
    #  @fn  generateOFSClientKeys(self,node_list=None,security_node=None)
    #
    #    Generate client SSH keys for OrangeFS security
    #    @param self The object pointer
    #    @param node_list List of nodes in network.
    #    @param security_node Node that generates server keys   
    
    def generateOFSClientKeys(self,node_list=None,security_node=None):
        if node_list is None:
            node_list = self.network_nodes
        if security_node is None:
            security_node = node_list[0]

        # cd /tmp/$USER/keys
        # for each client
        #   openSSl genrsa -out pvfs2-clientkey-{hostname}.pem 1024
        #   copy pvfs2-clientkey-{hostname).pem hostname:{orangefs}/etc
                
        
        output = []
       
        
        security_node.runSingleCommand("mkdir -p /tmp/%s/security" % security_node.current_user)
        security_node.changeDirectory("/tmp/%s/security" % security_node.current_user)

        for node in self.network_nodes:
            keyname = "pvfs2-clientkey-%s.pem" % node.hostname
            rc = security_node.runSingleCommand("openssl genrsa -out %s 1024" % keyname,output)
            if rc != 0:
                logging.exception("Could not create client security key for "+node.hostname)
                logging.exception(output) 
                return rc
            rc = security_node.copyToRemoteNode(source="/tmp/%s/security/%s" % (security_node.current_user,keyname), destination_node=node, destination="%s/etc/pvfs2-clientkey.pem" % node.ofs_installation_location, recursive=False)
            if rc != 0:
                logging.exception("Could not copy client security key %s for %s " % (keyname,node.hostname))
                logging.exception(output) 
                return rc


        return 0
    
   
    ##    
    #    @fn generateOFSKeystoreFile(self,node_list=None,security_node=None):
    #
    #    Generate OrangeFS keystore file for security
    #    @param self The object pointer
    #    @param node_list List of nodes in network.
    #    @param security_node Node that generates server keys

       

    
    def generateOFSKeystoreFile(self,node_list=None,security_node=None):
        if node_list is None:
            node_list = self.network_nodes
        if security_node is None:
            security_node = node_list[0]
        
        # cd /tmp/$USER/keys
        # for each server
        #   echo "S:{hostname} >> orangefs-keystore
        #   openssl rsa -in orangefs-serverkey.pem -pubout  >> orangefs_keystore
        # 
        # for each client 
        #   echo "C:{hostname} >> orangefs-keystore
        #   openssl rsa -in pvfs2clientkey.pem -pubout  >> orangefs_keystore
        
        # copy orangefs_keystore to all remote servers
        # 
        # sudo chown root:root /opt/orangefs/etc/pvfs2-clientkey.pem
        # sudo chmod 600 /opt/orangefs/etc/pvfs2-clientkey.pem
        
        output = []

        
        security_node.runSingleCommand("mkdir -p /tmp/%s/security" % security_node.current_user)
        security_node.changeDirectory("/tmp/%s/security" % security_node.current_user)
        
        # generate the keystore for entire network
        for node in self.network_nodes:
            
            server_keyname = "orangefs-serverkey-%s.pem" % node.hostname
            client_keyname = "pvfs2-clientkey-%s.pem" % node.hostname
            if node.alias_list is None:
                node.alias_list = node.getAliasesFromConfigFile(node.ofs_installation_location + "/etc/orangefs.conf")
            if len(node.alias_list) == 0:
                logging.exception( "Could not get aliases")
                return -1
            for alias in node.alias_list:
                if node.hostname in alias:
                    security_node.runSingleCommand('echo "S:%s" >> orangefs-keystore' % alias)
                    security_node.runSingleCommand('openssl rsa -in %s -pubout >> orangefs-keystore' % server_keyname)
                
            security_node.runSingleCommand('echo "C:%s" >> orangefs-keystore' % node.hostname)
            security_node.runSingleCommand('openssl rsa -in %s -pubout >> orangefs-keystore' % client_keyname)
            
        for node in self.network_nodes:

            rc = security_node.copyToRemoteNode(source="/tmp/%s/security/orangefs-keystore" % security_node.current_user, destination_node=node, destination="%s/etc/" % node.ofs_installation_location, recursive=False)
            if rc != 0:
                logging.exception( "Could not copy keystore for %s " % (node.hostname))
                logging.exception( output) 
                return rc
            #now protect the files
            rc = node.runSingleCommand("chmod 400 %s/etc/*.pem" % node.ofs_installation_location)
            if rc != 0:
                logging.exception("Could not protect keys on %s " % (node.hostname))
                logging.exception( output) 
                return rc

        
        return 0


  
    ##
    #  @fn  findExistingOFSInstallation(self,node_list=None):
    #
    #    find an existing OrangeFS installation for each node in the list.
    #
    #    @param self The object pointer
    #    @param node_list List of nodes in network.
    
     
    def findExistingOFSInstallation(self,node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        for node in node_list:
            rc = node.findExistingOFSInstallation()
            if rc != 0:
                return rc
        
        return 0
            
      
    ##
    #       @fn networkOFSSettings(self,
    #             ofs_installation_location,
    #             db4_prefix,
    #             ofs_extra_tests_location,
    #             pvfs2tab_file,
    #             resource_location,
    #             resource_type,
    #             ofs_config_file,
    #             ofs_fs_name,
    #             ofs_hostname_override,
    #             ofs_mount_point,
    #            ofs_protocol=None,
    #            ofs_source_location=None,
    #            openmpi_hosts_file=None,
    #            number_mpi_slots=1,
    #            node_list = None
    #            ):
    #
    #    Manually set OrangeFS settings for each node in the list. Used for retesting.
    #
    #    @param self The object pointer
    #    @param ofs_installation_location Directory where OrangeFS is installed. Should be the same on all nodes.
    #    @param db4_prefix Location of Berkeley DB4
    #    @param ofs_extra_tests_location Location of 3rd party benchmarks
    #    @param pvfs2tab_file Location of pvfs2tab file
    #    @param resource_location Location of OrangeFS source
    #    @param resource_type Form of source: TAR,SVN,LOCAL,BUILDNODE
    #    @param ofs_config_file Location of orangefs.conf file
    #    @param ofs_tcp_port TCP port on which OrangeFS servers run
    #    @param ofs_fs_name Name of OrangeFS in filesystem url
    #    @param ofs_hostname_override Change hostname to this. Needed to work around an openstack issue
    #    @param ofs_mount_point Location of OrangeFS mount_point
    #    @param ofs_protocol Network protocol for OrangeFS (ib or tcp)
    #    @param ofs_source_location Location where the OrangeFS source is located
    #    @param openmpi_hosts_file Location of the openmpi machinefile
    #    @param number_mpi_slots Number of MPI slots per node.
    #    @param node_list List of nodes in network
        
    def networkOFSSettings(self,
            ofs_installation_location,
            db4_prefix,
            ofs_extra_tests_location,
            pvfs2tab_file,
            resource_location,
            resource_type,
            ofs_config_file,
            ofs_tcp_port,
            ofs_fs_name,
            ofs_hostname_override = None,
            ofs_mount_point = None,
            ofs_protocol=None,
            ofs_source_location=None,
            openmpi_hosts_file=None,
            number_mpi_slots=1,
            node_list = None
            ):

        if node_list is None:
            node_list = self.network_nodes
            
        for i,node in enumerate(node_list):

            # source - Must provide location
            node.resource_location = resource_location
            node.resource_type = resource_type
            if resource_type == "BUILDNODE":
                node.ofs_source_location = resource_location

            
            
            if ofs_installation_location != None:
                node.ofs_installation_location = ofs_installation_location
            
            if ofs_source_location != None:
                node.ofs_source_location = ofs_source_location
            
            if db4_prefix != None:
                #rc = node.findDB4location
                node.db4_dir = db4_prefix
                node.db4_lib = db4_prefix+"/lib"

            # just reinstall extra tests
            if ofs_extra_tests_location != None:
                node.ofs_extra_tests_location = ofs_extra_tests_location
            
            if pvfs2tab_file != None:
                # find PVFS2TAB_FILE--or should we?
                node.setEnvironmentVariable("PVFS2TAB_FILE",pvfs2tab_file)
            
                
            # does OFS config file need to be provided?
            if ofs_config_file != None:
                node.ofs_conf_file = ofs_config_file
            
            if ofs_fs_name != None:
                node.ofs_fs_name = ofs_fs_name
            
            if ofs_tcp_port != None:
                node.ofs_tcp_port = ofs_tcp_port

            if ofs_protocol != None:
                node.ofs_protocol = ofs_protocol
            
            # Mount point. can be read from mount
            if ofs_mount_point != None:
                node.ofs_mount_point = ofs_mount_point
            
            if node.created_openmpihosts is None:
                if openmpi_hosts_file is None:
                    node.created_openmpihosts = "/home/%s/openmpihosts" % node.current_user
                else:
                    node.created_openmpihosts = openmpi_hosts_file
            
            node.number_mpi_slots = number_mpi_slots
                    
            # Hostname override. Needed to workaround an openstack problem.
            if len(ofs_hostname_override) > 0:
                try:
                    node.hostname = ofs_hostname_override[i]
                    node.runSingleCommandAsRoot("hostname "+node.hostname)
                except:
                    # if not, ignore the error
                    pass
            #node.setEnvironmentVariable("LD_LIBRARY_PATH",node.db4_lib+":"+node.ofs_installation_location+":$LD_LIBRARY_PATH")


  

    ##
    # @fn configureOpenMPI(self,mpi_nfs_directory=None,build_node=None,mpi_local_directory=None,node_list=None):
    #
    # This function installs OpenMPI software at the mpi_nfs_directory
    #
    # @param self The object pointer
    # @param build_node Node used to build OpenMPI
    # @param mpi_nfs_directory Location to install OpenMPI. This should be an nfs directory accessible from all nodes
    # @param mpi_local_directory Location to build OpenMPI. This should be a local directory on the build node
    # @param node_list List of nodes in OpenMPI network.
    
    

    def configureOpenMPI(self,mpi_nfs_directory=None,build_node=None,mpi_local_directory=None,node_list=None):
        if node_list is None:
            node_list = self.network_nodes
        if build_node is None:
            build_node = node_list[0]
        
        
        # the nfs directory is where all nodes will access MPI
        if mpi_nfs_directory is None:
            self.mpi_nfs_directory = "/opt/mpi"
      
        # the mpi local directory is where mpi will be built
        if mpi_local_directory is None:
            mpi_local_directory = "/opt/mpi"

        
        # build mpi in the build location, but install it to the nfs directory
        # Also download and build IOR benchmark.
        rc = build_node.configureOpenMPI(install_location=self.mpi_nfs_directory,build_location=mpi_local_directory)
    
        self.openmpi_version = build_node.openmpi_version
        
        build_node.changeDirectory(self.mpi_nfs_directory)
        
        for node in self.network_nodes:
            node.runSingleCommandAsRoot("chown -R  %s:%s %s" % (node.current_user,node.current_group,node.openmpi_source_location))


#         # we created an openmpihost file earlier. Now copy it to the appropriate directory.
#         if build_node.created_openmpihosts is None:
#             rc = build_node.runSingleCommand("/bin/cp %s %s" % (build_node.created_openmpihosts,self.mpi_nfs_directory))
#             if rc == 0:
#                 build_node.created_openmpihosts = self.mpi_nfs_directory + "/" + os.path.basename(build_node.created_openmpihosts)
#             
#         else:
#             #print 'grep -v localhost /etc/hosts | awk \'{print \\\$2 "\tslots=%r"}\' > %s/openmpihosts' % (slots,self.mpi_nfs_directory)
#             build_node.runSingleCommand("grep -v localhost /etc/hosts | awk '{print \$2 \"\\tslots=%r\"}' > %s/openmpihosts" % (slots,self.mpi_nfs_directory))
#             
        # Copy to all nodes with rsync
        self.copyOpenMPIToNodeList(node_list)


        for node in self.network_nodes:
#            node.setEnvironmentVariable("PATH","%s/openmpi/bin:%s/bin:\$PATH" % (self.mpi_nfs_directory,node.ofs_installation_location))
#            node.setEnvironmentVariable("LD_LIBRARY_PATH","%s/openmpi/lib:%s/lib64:%s/lib:%s/lib" % (self.mpi_nfs_directory,node.ofs_installation_location,node.ofs_installation_location,node.db4_dir))
            node.setEnvironmentVariable("PVFS2TAB_FILE","%s/etc/orangefstab" % node.ofs_installation_location)
            node.saveEnvironment()
        
        return rc


  
    
  
    ##
    # @fn   setupHadoop(self,hadoop_nodes=None,master_node=None):
    #
    #    Hadoop should be installed with required software. This configures hadoop 
    #    for OrangeFS testing on the virtual cluster.
    #
    # @param self The object pointer
    # @param hadoop_nodes Nodes on which to setup hadoop
    # @param master_node Hadoop master node
     
    def setupHadoop(self,hadoop_version="hadoop-2.6.0",hadoop_nodes=None,master_node=None):
        if hadoop_nodes is None:
            hadoop_nodes = self.network_nodes
        
        if master_node is None:
            master_node = hadoop_nodes[0]

        # Was originally set during installation, but now set here.
        master_node.hadoop_version = hadoop_version
        master_node.hadoop_location = "/opt/"+hadoop_version
        master_node.hadoop_examples_location = master_node.hadoop_location+"/share/hadoop/mapreduce/hadoop*examples*.jar"
        master_node.hadoop_test_location = master_node.hadoop_location+"/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-*-tests.jar"

        # remove list of slaves. We will be rebuilding it.
        master_node.runSingleCommand("rm %s/conf/slaves" % master_node.hadoop_location)


        for node in hadoop_nodes:
            
            node.hadoop_version = master_node.hadoop_version
            node.hadoop_location = "/opt/"+master_node.hadoop_version
            node.hadoop_examples_location = node.hadoop_location+"/share/hadoop/mapreduce/hadoop*examples*.jar"
            node.hadoop_test_location = node.hadoop_location+"/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-*-tests.jar"
            # copy templates to node
            #master_node.copyToRemoteNode(source="%s/test/automated/hadoop-tests.d/conf/" % master_node.ofs_source_location,destination_node=node,destination="%s/conf/" % node.hadoop_location,recursive=True)
            if master_node.hadoop_version == "hadoop-1.2.1":
                hadoop_conf=node.hadoop_location+"/conf"
                master_node.copyToRemoteNode(source="%s/src/client/hadoop/orangefs-hadoop1/src/main/resources/conf/" % master_node.ofs_source_location,destination_node=node,destination="%s/" % (hadoop_conf),recursive=True)
            else:
                hadoop_conf=node.hadoop_location+"/etc/hadoop"
                master_node.copyToRemoteNode(source="%s/src/client/hadoop/orangefs-hadoop2/src/main/resources/conf/" % master_node.ofs_source_location,destination_node=node,destination="%s/" % (hadoop_conf),recursive=True)
#              setup hadoop-env.sh
                     #JAVA_HOME should be set in the image.
            node.jdk6_location = node.runSingleCommandBacktick("echo \$JAVA_HOME")

#             node.runSingleCommand("echo 'export JAVA_HOME=%s' >> %s/conf/hadoop-env.sh" % (node.jdk6_location,node.hadoop_location))
#             node.runSingleCommand("echo 'export LD_LIBRARY_PATH=%s/lib' >> %s/conf/hadoop-env.sh" % (node.ofs_installation_location,node.hadoop_location))
#             node.runSingleCommand("echo 'export JNI_LIBRARY_PATH=%s/lib' >> %s/conf/hadoop-env.sh" % (node.ofs_installation_location,node.hadoop_location))
#             node.runSingleCommand("echo 'export HADOOP_CLASSPATH=\$JNI_LIBRARY_PATH/orangefs-hadoop1-2.9.0.jar:\$JNI_LIBRARY_PATH/ofs-jni-2.9.0.jar' >> %s/conf/hadoop-env.sh" % node.hadoop_location)
            
            # update environment
            node.runSingleCommandAsRoot('sed -i s,__HADOOP_VERSION__,%s,g /etc/profile.d/path_additions.sh' % node.hadoop_version)
            node.runSingleCommandAsRoot('sed -i s,__HADOOP_VERSION__,%s,g /etc/profile.d/hadoop_env.sh' % node.hadoop_version)
            
            node.runSingleCommand('sed -i s,/usr/lib/jvm/java-7-openjdk-amd64,%s,g %s/hadoop-env.sh' % (node.jdk6_location,hadoop_conf ))
            
            node.runSingleCommand('sed -i s,/opt/orangefs-trunk,%s,g %s/hadoop-env.sh' % (node.ofs_installation_location,hadoop_conf ))
            node.runSingleCommand("echo 'export ORANGEFS_STRIP_SIZE_AS_BLKSIZE=true' >> %s/hadoop-env.sh" % hadoop_conf)
            # update core-site.xml
            node.runSingleCommand("sed -i s,/mnt/orangefs,%s,g %s/core-site.xml" % (node.ofs_mount_point,hadoop_conf))
            # Core site points to the OrangeFS on the master node
            node.runSingleCommand("sed -i s,localhost-orangefs:3334,%s:%d,g %s/core-site.xml" % (master_node.hostname,master_node.ofs_tcp_port,hadoop_conf))
            
            # update mapred-site.xml
            node.runSingleCommand("sed -i s,localhost-orangefs:3334,%s:%d,g %s/mapred-site.xml" % (node.hostname,node.ofs_tcp_port,hadoop_conf))
            node.runSingleCommand("sed -i s/localhost/%s/g %s/mapred-site.xml" % (master_node.hostname,hadoop_conf))
            
            node.runSingleCommand("sed -i s/localhost/%s/g %s/yarn-site.xml" % (master_node.hostname,hadoop_conf))
            node.runSingleCommand("sed -i s/yarn.nodemanager.hostname/commentout.yarn.nodemanager.hostname/ %s/yarn-site.xml" % hadoop_conf)
            
            # point slave node to master
            node.runSingleCommand("echo '%s' > %s/masters" % (master_node.hostname,hadoop_conf))
            
            
            
            
            # notify master of new slave
            master_node.runSingleCommand("echo '%s' >> %s/slaves" % (node.hostname,hadoop_conf))
        
        if master_node.hadoop_version == "hadoop-1.2.1":    
            master_node.runSingleCommand("%s/bin/start-mapred.sh" % master_node.hadoop_location)
        else:
            master_node.runSingleCommand("%s/src/client/hadoop/orangefs-hadoop2/scripts/examples/hadoop/start_hadoop.sh" % master_node.ofs_source_location)
            
        time.sleep(20)
        # hadoop dfs -ls is our "ping" for hadoop. 
        rc = master_node.runSingleCommand("%s/bin/hadoop dfs -ls /" % master_node.hadoop_location)
        if rc != 0:
            print "Hadoop setup failed. See logs for more information."
        else:
            print "Hadoop setup successfully"
            master_node.runSingleCommand("%s/bin/hadoop dfs -mkdir -p /user/%s" % (master_node.hadoop_location,master_node.current_user))
            
        return rc
    
    ##
    # @fn printNetwork(self):
    #
    # Prints the python dictionary of all nodes on the network. For debugging.
    #
    # @param self the object pointer
    #
    #
    
    def printNetwork(self):
        
        print "==========================================================================="
        print "Virtual Cluster: Network-wide settings"
        pprint(self.__dict__)
        for node in self.network_nodes:
            print "------------------------------------------------------------------------"
            print "Node settings for %s" %  node.ip_address
            pprint(node.__dict__)
        
        print "==========================================================================="
        
        return 0
    
    ##
    # @fn checkNetwork(self):
    #
    # Checks connectivity between the nodes in the network.
    #
    # @param self the object pointer
    #
    #
        
    def checkNetwork(self):
        
        print "==========================================================================="
        print "Testing network connectivity"
        
        failed = 0
        for srcnode in self.network_nodes:
            for destnode in self.network_nodes:
                rc = srcnode.runSingleCommandAsRoot("ping -c 1 %s" % destnode.hostname)
                if rc != 0:
                    print "Could not ping %s from %s." % (destnode.hostname,srcnode.hostname)
                    failed = failed + 1
        
        print "==========================================================================="
                    
       
        
        return failed
  
    ##
    # @fn checkExternalConnectivity(self):
    #
    # Checks connectivity to the nodes in the network from the local machine via ping
    #
    # @param self the object pointer
    #
    #
    
    def checkExternalConnectivity(self):
        rc = 0
        for node in self.network_nodes:
            rc += self.local_master.runSingleCommandAsRoot("ping -c 1 %s" % node.ext_ip_address )
        return rc
    
    ##
    # @fn getInstanceList()
    #
    # Creates node instances from cloud (AWS) instance list
    #
    # @param self the object pointer
    # @param logfile List of AWS instances.
    #
    #
    
    def getInstanceList(self,logfile=None):
        
        if logfile is None:
            logfile = self.logfile
        nodes = []
        if os.path.exists(logfile):
            input = open(logfile,"r")
            for line in input:
                nodes.append(line.rstrip())
        return nodes