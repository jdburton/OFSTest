# !/usr/bin/python
##
# @class OFSTestMain
#
# @brief This class drives the OrangeFS testing. This sets up OrangeFS on the OFSTestNetwork based on the OFSTestConfig.
#
#

# Members:
#
# OFSTestConfig self.config = Testing configuration. 
# OFSTestNework self.network = Virtual cluster.
#
# Methods:
#
#   setConfig()     Sets self.config based on info from the command line, 
#                   config file, etc.
#
#   initNetwork()   builds the OFSTestNetwork virtual cluster based on the
#                   config values.
#
#   checkNetwork()  verify that the OFSTestNetwork has all the information to setup OrangeFS
#
#   printConfig()   Prints the dictionary of self.config. For debugging.
#
#   setupOFS()      Builds the OFSTestNetwork as specified by the config.
#
#   checkOFS()      Verify the OrangeFS installation is complete and system has all information needed to run OrangeFS tests.
#
#   runTest()       Runs the tests for OrangeFS as specified by the config.
#


import OFSTestConfig
import OFSTestConfigFile
import OFSTestConfigMenu
import OFSTestNetwork
import time
import sys
import traceback
from pprint import pprint
import logging

class OFSTestMain(object):
    
    ##
    #
    # @fn __init__(self,config):
    #
    # @brief Sets the config and initializes the network class.
    #
    # @param self The object pointer
    # @param config an OFSTestConfig object that represents the test configuration. 

    
    def __init__(self,config):

        # Class Members:

        ##
        # @var self.config  
        # OFSTestConfig Testing configuration.
        self.config = config 
        
        # @var self.network 
        # OFSTestNework Virtual cluster.

        self.ofs_network = OFSTestNetwork.OFSTestNetwork()
        
        

        
        


    ##
    #
    # @fn setConfig(self,**kwargs):
    #
    # @brief Sets self.config based on info from the command line, config file, etc.
    #
    # @param self The object pointer
    # @param kwargs Dictionary with configuration variable,value pairs. See OFSTestConfig for possible values.



    def setConfig(self,**kwargs):
        self.config.setConfig(**kwargs)
    
    ##
    #  @fn printConfig(self):
    #   
    # Prints the dictionary of self.config. For debugging.
    #
    # @param self The object pointer
    
    
    def printConfig(self):
        self.config.printDict()

    ##
    # @fn writeOutput(self,filename,function,rc):   
    #
    # Writes the output of a test to the output file. If test function returns 0, assume success, otherwise, failure.
    #
    # @param self The object pointer
    # @param filename Name of output file
    # @param function Function that was tested.
    # @param rc  Return code of the tested function
    #    

    def writeOutput(self,filename,function,rc):
        output = open(filename,'a+')
        if rc != 0:
            output.write("%s........................................FAIL: RC = %r\n" % (function.__name__,rc))
        else:
            output.write("%s........................................PASS.\n" % function.__name__)
        output.close()
    

    
    ##
    # @fn initNetwork(self)
    #
    # @brief Builds the OFSTestNetwork virtual cluster based on the config values.
    #
    # @param self The object pointer
    
    def initNetwork(self):

    # if the configuration says that we need to create new Cloud nodes, 
        # do it.
        if self.config.number_new_cloud_nodes > 0:
            self.setupNewCloudCluster()
        # If config.node_ip_addresses > 0, then we are dealing with existing 
        # nodes. Add them to the virtual cluster.
        elif len(self.config.node_ip_addresses) > 0:
            self.setupExistingCluster()
        
        else:
            print "Cannot create test cluster. %d new cloud nodes and %d existing nodes specified" % (self.config.number_new_cloud_nodes,len(self.config.node_ip_addresses))
        
        
        # TODO: Make this smart enough to return success or failure.
        
        return self.checkNetwork()
        
        
        

    ##
    # @fn checkOFS(self)
    #
    # checks to see if OrangeFS is setup on the cluster.
    # Assumes that all work has been done to setup OrangeFS 
    #
    # @param self The object pointer
    #
    # @return 0 OrangeFS setup
    # @return Not 0 OrangeFS not setup

    
    def checkOFS(self):
        
        
    
        # TODO: Make this smart enough to detect if the installation is running
        print "Looking for existing OrangeFS installation"
        rc = self.ofs_network.findExistingOFSInstallation()
        if rc != 0:
            print "Existing OrangeFS installation not found."
            return rc

        # OK, now that OrangeFS installation has been found, set the
        # appropriate varaibles in the OFSTestNetwork virtual cluster.
        print "Existing OrangeFS installation found. Detecting settings"
        self.ofs_network.networkOFSSettings(
            ofs_installation_location = self.config.install_prefix,
            db4_prefix=self.config.db4_prefix,
            ofs_extra_tests_location=self.config.ofs_extra_tests_location,
            pvfs2tab_file=self.config.ofs_pvfs2tab_file,
            resource_location=self.config.ofs_resource_location,
            resource_type=self.config.ofs_resource_type,
            ofs_config_file=self.config.ofs_config_file,
            ofs_tcp_port=self.config.ofs_tcp_port,
            ofs_fs_name=self.config.ofs_fs_name,
            ofs_hostname_override=self.config.ofs_hostname_override,
            ofs_mount_point=self.config.ofs_mount_point
            )
        
        '''
        # TODO: Start OFS Server and client if they haven't been started.
        # Is this necessary?
        
        print ""
        print "==================================================================="
        print "Start OFS Server"
        
        rc = self.ofs_network.startOFSServers()

        print ""
        print "==================================================================="
        print "Start OFS Client"
        rc = self.ofs_network.startOFSClientAllNodes(security=self.config.ofs_security_mode)

        '''
        return 0

    ##
    # @fn checkOFS(self)
    #
    # checks to see if network has been properly setup 
    #
    # @param self The object pointer
    #
    # @return 0 network setup
    # @return Not 0 network not setup


    
    def checkNetwork(self):
    
        return self.ofs_network.checkNetwork()
        
    ##
    # @fn setupNewCloudCluster(self):      
    #
    #    Builds the OFSTestNetwork as specified by the config.
    #
    # @param self The object pointer
        
    def setupNewCloudCluster(self):
    
        # First, if we're using Cloud/Openstack, open the connection
        print "===========================================================" 
        print "Connecting to EC2/OpenStack cloud using information from " + self.config.cloud_config
        #print "%s,%s,%s,%s,%s" % (self.config.cloud_config,self.config.cloud_key_name,self.config.ssh_key_filepath,self.config.cloud_type,self.config.nova_password_file)
        self.ofs_network.addCloudConnection(self.config.cloud_config,self.config.cloud_key_name,self.config.ssh_key_filepath,self.config.cloud_type,self.config.nova_password_file,self.config.cloud_region)


        print "===========================================================" 
        print "Creating %d new EC2/OpenStack cloud nodes" % self.config.number_new_cloud_nodes
        self.ofs_network.createNewCloudNodes(self.config.number_new_cloud_nodes,self.config.cloud_image,self.config.cloud_machine,self.config.cloud_associate_ip,self.config.cloud_domain,self.config.cloud_subnet,self.config.instance_suffix,self.config.cloud_image_id,self.config.cloud_security_group_ids,self.config.spot_instance_bid)
    
                
        # Upload the access key to all the nodes in the cluster.
        print "===========================================================" 
        print "Distributing SSH keys"
        self.ofs_network.uploadKeys()

        # Sometimes virtual networking doesn't do a good job of letting the
        # hosts find each other. This method sets standard hostnames and 
        # updates the /etc/hosts file of each virtual node so that everyone 
        # can find everyone else.
        print "===========================================================" 
        print "Verifying hostname resolution"
        self.ofs_network.updateEtcHosts()


        # MPI and Hadoop testing require passwordless SSH access.
        print "===========================================================" 
        print "Enabling Passwordless SSH access"
        self.ofs_network.enablePasswordlessSSH()
        #print "Enabling Passwordless SSH access for root"
        #self.ofs_network.enablePasswordlessSSH(user="root")

        # Update new cloud nodes and reboot. We don't want to do this with real nodes 
        # because we don't want to step on the admin's toes.
        print ""
        print "==================================================================="
        print "Updating New Nodes (This may take awhile...)"
        self.ofs_network.updateCloudNodes(custom_kernel=self.config.custom_kernel,kernel_git_location=self.config.kernel_git_location, kernel_git_branch=self.config.kernel_git_branch)
 
 
        print "===========================================================" 
        print "Installing required OrangeFS software from "+ self.config.url_base
        self.ofs_network.setUrlBase(self.config.url_base)
       

#                 # Install software required to compile and run OFS and all tests.
#         print ""
#         print "==================================================================="
#         print "Installing Hadoop"
#         self.ofs_network.installHadoop()


    ##
    # @fn setupExistingCluster(self):      
    #
    #    Builds the OFSTestNetwork as specified by the config.
    #    Assumes that nodes have been updated, all software has been installed and that network access is working. 
    #
    # @param self The object pointer
        
    def setupExistingCluster(self):

        print "===========================================================" 
        print "Adding %d Existing Nodes to OFS cluster" % len(self.config.node_ip_addresses)

        for i in range(len(self.config.node_ip_addresses)):
            
            # For each node, check to see if test program is accessing
            # through external address. If so, set the external address.

            if len(self.config.node_ext_ip_addresses) > 0:
                ext_ip_address = self.config.node_ext_ip_addresses[i]
            else:
                # if not, underlying functionality will use one IP for both.
                ext_ip_address = None

            # Add the node to the virtual cluster.
            self.ofs_network.addRemoteNode(ip_address=self.config.node_ip_addresses[i],username=self.config.node_usernames[i],key=self.config.ssh_key_filepath,is_cloud=self.config.using_cloud,ext_ip_address=ext_ip_address)
        
        print "===========================================================" 
        print "Installing required OrangeFS software from "+ self.config.url_base
        self.ofs_network.setUrlBase(self.config.url_base)


    ##
    # @fn setupOFS(self):      
    #
    #    Builds the OFSTestNetwork as specified by the config.
    #
    # @param self The object pointer
        
    def setupOFS(self):


        print ""
        print "==================================================================="
        print "Downloading and building OrangeFS from %s resource %s" % (self.config.ofs_resource_type,self.config.ofs_resource_location)
        rc = self.ofs_network.buildOFSFromSource(
        resource_type=self.config.ofs_resource_type,
        resource_location=self.config.ofs_resource_location,
        build_kmod=self.config.ofs_build_kmod,
        enable_strict=self.config.enable_strict,
        enable_fuse=self.config.install_fuse,
        enable_shared=self.config.install_shared,
        enable_hadoop=self.config.install_hadoop,
        ofs_prefix=self.config.install_prefix,
        db4_prefix=self.config.db4_prefix,
        ofs_patch_files=self.config.ofs_patch_files,
        configure_opts=self.config.configure_opts,
        security_mode=self.config.ofs_security_mode,
        debug=self.config.ofs_compile_debug,
        svn_options=self.config.svn_options,
        hadoop_version=self.config.hadoop_version,
        ofs_database=self.config.ofs_database,
        svn_username=self.config.svn_username,
        svn_password=self.config.svn_password
        )
        
        if rc != 0:
            print "Could not build OrangeFS. Aborting."
            return rc
        
        print ""
        print "==================================================================="
        print "Installing OrangeFS to "+self.config.install_prefix
        rc = self.ofs_network.installOFSBuild(install_opts=self.config.install_opts)
        if rc != 0:
            print "Could not install OrangeFS. Aborting."
            return rc


        # Cert based security must be done before copy. Key based must be done after copy. 
        if self.config.ofs_security_mode is None:
            if self.config.ofs_security_mode.lower() == "cert":
                print ""
                print "==================================================================="
                print "Generating OrangeFS security certificates"
                rc = self.ofs_network.generateOFSCertificates(self.config.ldap_server_uri,self.config.ldap_admin,self.config.ldap_admin_password,self.config.ldap_container)

        print ""
        print "==================================================================="
        print "Configure OrangeFS Server"
        rc = self.ofs_network.configureOFSServer(
                                                 ofs_fs_name=self.config.ofs_fs_name,
                                                 pvfs2genconfig_opts=self.config.pvfs2genconfig_opts,
                                                 security=self.config.ofs_security_mode,
                                                 ofs_data_location = self.config.ofs_data_location,
                                                 ofs_metadata_location = self.config.ofs_metadata_location,
                                                 dedicated_metadata_server=self.config.dedicated_metadata_server,
                                                 dedicated_client=self.config.dedicated_client,
                                                 servers_per_node=self.config.servers_per_node
                                                 )

        if rc != 0:
            print "Could not configure OrangeFS servers. Aborting."
            return rc



        if self.config.install_MPI == True or self.config.run_mpi_tests == True:
            print ""
            print "==================================================================="
            print "Install OpenMPI"
            self.ofs_network.configureOpenMPI()

        

        if self.config.install_tests:
            print ""
            print "==================================================================="
            print "Installing OrangeFS Tests"
            rc = self.ofs_network.installOFSTests(configure_options=self.config.configure_opts)
            if rc != 0:
                print "Could not install OrangeFS tests. Aborting."
                return rc

            print ""
            print "==================================================================="
            print "Installing Third-Party Benchmarks"
            rc = self.ofs_network.installBenchmarks()
            if rc != 0:
                print "Could not install third-party benchmarks. Aborting."
                return rc

        print ""
        print "==================================================================="
        print "Copy installation to all nodes"
        # TODO: Should handle this with exceptions.
        rc = self.ofs_network.copyOFSToNodeList()

        if self.config.ofs_security_mode:
            if self.config.ofs_security_mode.lower() == "key":
                print ""
                print "==================================================================="
                print "Generating OrangeFS security keys"

                rc = self.ofs_network.generateOFSKeys()


                    
        
        print ""
        print "==================================================================="
        print "Start OFS Server"
        rc = self.ofs_network.startOFSServers()
        #TODO: Need to handle error conditions
        
        print ""
        print "==================================================================="
        print "Start OFS Client"
        rc = self.ofs_network.startOFSClientAllNodes(security=self.config.ofs_security_mode,disable_acache=self.config.ofs_disable_acache)


        if self.config.install_hadoop == True or self.config.run_hadoop_tests == True:
            print ""
            print "==================================================================="
            print "Setup Hadoop"
            self.ofs_network.setupHadoop(hadoop_version=self.config.hadoop_version)
        
        
        return self.checkNetwork()

    ##
    #
    # @fn writeOutputHeader(self,filename,header,mode='a+'):
    #
    # Writes the output header to the file.
    #
    # @param self The object pointer
    # @param filename The file to write the message
    # @param header The message to write in the header
    # @param mode Mode to open the file. Default is append (a+).
    #

    def writeOutputHeader(self,filename,header,mode='a+'):
        output = open(filename,mode)
        output.write("%s ==================================================\n" % header)
        output.close()
    
    ##
    # @fn   runTest(self):       
    #
    # Runs the tests for OrangeFS as specified by the config. 
    #
    # @param self The object pointer
    
    # TODO: Reimpliment this.


    def runTest(self):
        
        # Good debug information.
        #print "Printing dictionary of master node"
        #pprint(self.ofs_network.network_nodes[0].__dict__)
        
        print ""
        print "==================================================================="
        print "Run Tests"
        

        # TODO: Move this section to OFSTestNetwork

        # Results filename is specified in the config.
        filename = self.config.log_file
        mount_type = "kmod"
        
        rc = 0

        # head_node is the first node in the cluster. This is the node from 
        # where all the tests will be run.
        head_node = self.ofs_network.network_nodes[0]
        
        # Set the LD_LIBRARY_PATH and LIBRARY_PATH on the head node
        # TODO: Do we still need to do this?
        if self.config.run_mpi_tests == True:
            head_node.setEnvironmentVariable("LD_LIBRARY_PATH","/opt/db4/lib:%s/lib64:%s/lib:%s/lib" % (head_node.ofs_installation_location,head_node.ofs_installation_location,head_node.openmpi_installation_location))
        else:
            head_node.setEnvironmentVariable("LD_LIBRARY_PATH","/opt/db4/lib:%s/lib64:%s/lib" % (head_node.ofs_installation_location,head_node.ofs_installation_location))
    
        # Go home.
        head_node.changeDirectory("~")

        # Print the header in the output file. Overwrite previous.
        self.writeOutputHeader(filename,"Running OrangeFS Tests",'w+')

        # Run the sysint tests, if required.
        if self.config.run_sysint_tests == True:
            # Sysint tests are located in OFSSysintTest
            import OFSSysintTest
            
            # Start the OrangeFS Client on the head node
            rc = self.ofs_network.startOFSClientAllNodes(security=self.config.ofs_security_mode,disable_acache=self.config.ofs_disable_acache)
        
            # print section header in output file.
            self.writeOutputHeader(filename,"Sysint Tests")
            

            # The list of sysint tests to run is found in OFSSysintTest.test.
            # This is an array of strings that correspond to function names.
            # The functions are run in the order they are listed in the array.
            for callable in OFSSysintTest.tests:
                try:
                    rc = head_node.runOFSTest("sysint",callable)
                    self.writeOutput(filename,callable,rc)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    traceback.print_exc()
                    if self.config.stop_on_failure == True:
                        return -888
                    pass
                if rc != 0 and self.config.stop_on_failure == True:
                    return rc

        # Run the kmod vfs tests, if required.
        if self.config.run_vfs_tests == True or self.config.run_vfs_benchmarks == True:
            # vfs tests are located in OFSVFSTest
            # The same tests are used for both kmod-vfs and fuse.
            import OFSVFSTest
        
            # specify "kmod" tests.
            mount_type = "kmod"
            # Start the OrangeFS Client on the head node

            rc = self.ofs_network.startOFSClientAllNodes(security=self.config.ofs_security_mode,disable_acache=self.config.ofs_disable_acache)


            # OrangeFS must be mounted to run kmod tests.
            # unmount, just in case.
            self.ofs_network.unmountOFSFilesystemAllNodes();
            # mount, not with fuse.
            self.ofs_network.mountOFSFilesystemAllNodes(mount_fuse=False)
            # Make sure filesystem is mounted or we will get false positives.
            rc = head_node.checkMount()
            
            if rc != 0:
                self.writeOutputHeader(filename,"VFS Tests (%s) could not run. Mount failed." % mount_type)           
                # Each test should fail. Use error -999 to indicate mount failure.
                for callable in OFSVFSTest.tests:
                    self.writeOutput(filename,callable,-999)
                if self.config.stop_on_failure == True:
                    return -999

            if self.config.run_vfs_tests == True:
                # if everything is good, run the test.
                
                    # print section header in output file.
                    self.writeOutputHeader(filename,"VFS Tests (%s)" % mount_type)
    
    
                    # The list of vfs tests to run is found in OFSVFSTest.test.
                    # This is an array of strings that correspond to function names.
                    # The functions are run in the order they are listed in the array.
                    for callable in OFSVFSTest.tests:
                        try:
                            rc = head_node.runOFSTest("vfs-%s" % mount_type,callable)
                            self.writeOutput(filename,callable,rc)
                        except:
                            print "Unexpected error:", sys.exc_info()[0]
                            traceback.print_exc()
                            if self.config.stop_on_failure == True:
                                return -888
                            pass
                        if rc != 0 and self.config.stop_on_failure == True:
                            return rc
                            # if not, print failure.


                        
            if self.config.run_vfs_benchmarks == True:
                import OFSVFSBenchmarks
                if rc == 0:
                    # print section header in output file.
                    self.writeOutputHeader(filename,"VFS Benchmarks (%s)" % mount_type)
    
    
                    # The list of vfs tests to run is found in OFSVFSTest.test.
                    # This is an array of strings that correspond to function names.
                    # The functions are run in the order they are listed in the array.
                    for callable in OFSVFSBenchmarks.tests:
                        try:
                            rc = head_node.runOFSTest("vfs-%s" % mount_type,callable)
                            self.writeOutput(filename,callable,rc)
                        except:
                            print "Unexpected error:", sys.exc_info()[0]
                            traceback.print_exc()
                            if self.config.stop_on_failure == True:
                                return -888
                            pass
                        if rc != 0 and self.config.stop_on_failure == True:
                            return rc

                else:
                    self.writeOutputHeader(filename,"VFS Tests (%s) could not run. Mount failed." % mount_type)           
                    # Each test should fail. Use error -999 to indicate mount failure.
                    for callable in OFSVFSTest.tests:
                        self.writeOutput(filename,callable,-999)
                    if self.config.stop_on_failure == True:
                        return -999



        
        # run fuse tests, if required.
        if self.config.run_fuse_tests == True:
            # fuse tests are almost identical to kmod-vfs tests.
            # The only difference is that the OrangeFS client is NOT running and 
            # the filesystem is mounted with the fuse module instead of kmod.
            # The same tests are used for both kmod-vfs and fuse.
            import OFSVFSTest
            
            
            # specify "kmod" tests.
            mount_type = "fuse"
            # OrangeFS must be mounted to run kmod tests.
            # unmount, just in case.
            self.ofs_network.unmountOFSFilesystemAllNodes();
            # mount, not with fuse.
            self.ofs_network.mountOFSFilesystemAllNodes(mount_fuse=True)  
            # Make sure filesystem is mounted or we will get false positives.
            rc = head_node.checkMount()

            # if everything is good, run the test.
            if rc == 0:
                
                self.writeOutputHeader(filename,"VFS Tests (%s)" % mount_type)

                # The list of vfs tests to run is found in OFSVFSTest.test.
                # This is an array of strings that correspond to function names.
                # The functions are run in the order they are listed in the array.
                for callable in OFSVFSTest.tests:
                    try:
                        rc = head_node.runOFSTest("vfs-%s" % mount_type,callable)
                        self.writeOutput(filename,callable,rc)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        traceback.print_exc()
                        if self.config.stop_on_failure == True:
                            return -888

                        pass
                    if rc != 0 and self.config.stop_on_failure == True:
                        return rc

                

        
            else:
                self.writeOutputHeader(filename,"VFS Tests (%s) could not run. Mount failed." % mount_type)           
                # Each test should fail. Use error -999 to indicate mount failure.
                for callable in OFSVFSTest.tests:
                    self.writeOutput(filename,callable,-999)
                if self.config.stop_on_failure == True:
                    return -999



        # run the usrint tests, if required.
        if self.config.run_usrint_tests == True:
            # usrint tests are located in OFSUsrintTest

            import OFSUsrintTest

            # TODO: Check to see if usrint and fuse are compatible.
            if False:
                self.writeOutputHeader(filename,"Usrint Tests not compatible with fuse=====================================\n")
            else:
                # Unmount OrangeFS and stop the OrangeFS client.
                self.ofs_network.unmountOFSFilesystemAllNodes()
                self.ofs_network.stopOFSClientAllNodes()
                self.writeOutputHeader(filename,"Usrint Tests")
                
                # The list of usrint tests to run is found in OFSUsrintTest.test.
                # This is an array of strings that correspond to function names.
                # The functions are run in the order they are listed in the array.
                for callable in OFSUsrintTest.tests:
                    try:
                        rc = head_node.runOFSTest("usrint",callable)
                        self.writeOutput(filename,callable,rc)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        traceback.print_exc()
                        if self.config.stop_on_failure == True:
                            return -888

                        pass
                    if rc != 0 and self.config.stop_on_failure == True:
                        return rc

                
        # run the mpi tests, if required.
        if self.config.run_mpi_tests == True or self.config.run_mpi_benchmarks == True:
            
            # Remount OrangeFS
            self.ofs_network.unmountOFSFilesystemAllNodes()
            self.ofs_network.mountOFSFilesystemAllNodes(mount_fuse=False)
            
            if self.config.run_mpi_tests == True:
            
                self.writeOutputHeader(filename,"MPI VFS Tests (%s)" % mount_type)
                
                import OFSMpiVFSTest
                
                for callable in OFSMpiVFSTest.tests:
                    try:
                        rc = head_node.runOFSTest("mpivfs-%s" % mount_type,callable)
                        self.writeOutput(filename,callable,rc)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        traceback.print_exc()
                        if self.config.stop_on_failure == True:
                            return -888
                        pass
    
                    if rc != 0 and self.config.stop_on_failure == True:
                        return rc
                
                self.writeOutputHeader(filename,"MPI-IO Tests")
    
                # The list of mpiio tests to run is found in OFSMpiioTest.test.
                # This is an array of strings that correspond to function names.
                # The functions are run in the order they are listed in the array.
                import OFSMpiioTest
                
                for callable in OFSMpiioTest.tests:
                    try:
                        rc = head_node.runOFSTest("mpiio", callable)
                        self.writeOutput(filename,callable,rc)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        traceback.print_exc()
                        if self.config.stop_on_failure == True:
                            return -888
                        pass
                    if rc != 0 and self.config.stop_on_failure == True:
                        return rc
                
            
            if self.config.run_mpi_benchmarks:
                self.writeOutputHeader(filename,"MPI-Benchmarks")
                
                import OFSMpiBenchmarks
    
                # The list of mpiio tests to run is found in OFSMpiBenchmarks.test.
                # This is an array of strings that correspond to function names.
                # The functions are run in the order they are listed in the array.
                for callable in OFSMpiBenchmarks.tests:
                    try:
                        rc = head_node.runOFSTest("mpi-bench", callable)
                        self.writeOutput(filename,callable,rc)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        traceback.print_exc()
                        if self.config.stop_on_failure == True:
                            return -888
                        pass
                    if rc != 0 and self.config.stop_on_failure == True:
                        return rc


        # run the hadoop tests, if required.
        if self.config.run_hadoop_tests == True:
            
            # run the hadoop tests, if required.
            import OFSHadoopTest
            
            # Unmount OrangeFS and stop the OrangeFS client.
            self.ofs_network.unmountOFSFilesystemAllNodes()
            self.ofs_network.stopOFSClientAllNodes()

            self.writeOutputHeader(filename,"Hadoop Tests")
            
            # The list of hadoop tests to run is found in OFSHadoopTest.test.
            # This is an array of strings that correspond to function names.
            # The functions are run in the order they are listed in the array.

            for callable in OFSHadoopTest.tests:
                try:
                    rc = head_node.runOFSTest("hadoop", callable)
                    self.writeOutput(filename,callable,rc)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    traceback.print_exc()
                    if self.config.stop_on_failure == True:
                        return -888
                    
                    pass
                if rc != 0 and self.config.stop_on_failure == True:
                    return rc


        # run miscellaneous tests after run.
        if True == True:
            
            
            import OFSMiscPostTest
            
            # Unmount OrangeFS and stop the OrangeFS client.
            self.ofs_network.unmountOFSFilesystemAllNodes()
            self.ofs_network.stopOFSClientAllNodes()

            self.writeOutputHeader(filename,"Misc Tests (Post run)")
            
            # The list of misc tests to run is found in OFSMiscPostTest.test.
            # This is an array of strings that correspond to function names.
            # The functions are run in the order they are listed in the array.

            for node in self.ofs_network.network_nodes:
                for callable in OFSMiscPostTest.tests:
                    try:
                        rc = node.runOFSTest("misc-post", callable)
                        self.writeOutput(filename,callable,rc)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        traceback.print_exc()
                        if self.config.stop_on_failure == True:
                            return -888
                        pass
                    if rc != 0 and self.config.stop_on_failure == True:
                        return rc
        

        # Test runfunction group
        # TODO: Remove this.
#        try:
#            self.runFunctionGroup("OFSHadoopTest")
#        except:
#            "runFunctionGroup didn't work. Oh well"
#            traceback.print_exc()
#
#
#        if self.config.cloud_delete_after_test == True:
#            print ""
#            print "==================================================================="
#            print "Terminating Nodes"
#            self.ofs_network.terminateAllCloudNodes()

    def terminateAllCloudNodes(self):
            print ""
            print "==================================================================="
            print "Terminating Nodes"
            self.ofs_network.terminateAllCloudNodes()


    def stopAllCloudNodes(self):
            print ""
            print "==================================================================="
            print "Stopping Nodes"
            self.ofs_network.stopAllCloudNodes()
        
    ##
    #
    # @fn runFunctionGroup(self,function_group_name):
    #
    # Run a function group. Function groups are in separate files with appropriate test functions in them.
    # For example, OFSSysintTest.py contains the OFSSysintTest function group that tests the system integration functions.
    #
    # @param self The object pointer
    # @param function_group_name The name of the python namespace that contains the function. This should be the same as the python file that contains the functions without the .py extension.

    def runFunctionGroup(self,function_group_name):
        
        print function_group_name
        function_group = getattr(__import__(function_group_name),function_group_name)
        
        self.writeOutputHeader(self.config.log_file,function_group.header)
        
        for callable in function_group.tests:
            try:
                rc = self.ofs_network.runOFSTest(function_group.prefix, callable)
                self.writeOutput(self.config.filename,callable,rc)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                traceback.print_exc()
                pass


    def restartOFS(self):
        
        self.ofs_network.unmountOFSFilesystemAllNodes()
        self.ofs_network.stopOFSClientAllNodes()
        self.ofs_network.startOFSClientAllNodes(security=self.config.ofs_security_mode,disable_acache=self.config.ofs_disable_acache)
        self.ofs_network.mountOFSFilesystemAllNodes()
    
    def doPostTest(self):
    
        try:
            if self.config.cloud_delete_after_test or self.config.spot_instance_bid.lower() == "auto" or float(self.config.spot_instance_bid):
                print "Test complete. Deleting all cloud nodes."
                self.terminateAllCloudNodes()
        
        except ValueError:
        
            if self.config.restart_ofs == True:
                print "Test complete. Restarting OrangeFS clients and servers"
                self.restartOFS()
            else:
                self.stopAllCloudNodes()
