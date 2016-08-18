#!/usr/bin/python
#
# @namespace OFSVFSBenchmarks
#
# @brief This class implements tests to be run on the virtual file system when mounted via kernel module or fuse. 
#
#
# @var  header 
# Name of header printed in output file
# @var  prefix  
# Name of prefix for test name
# @var  run_client  
# Do we need to run the PVFS2 client?
# @var  mount_fs  
# Does the file system need to be mounted?
# @var  mount_as_fuse
# Do we mount it via fuse?
# @var  tests  
# List of test functions (at end of file)
#
#


import inspect
from datetime import datetime

header = "OFS VFS Benchmarks(kmod)"
prefix = "vfs-bench-kmod"
mount_fs = True
run_client = True
mount_as_fuse = False
debug = True


#------------------------------------------------------------------------------
#  
# Test functions
#
# All functions MUST have the following parameters and return code convention.
#
#   params:
#
#   testing_node = OFSTestNode on which the tests will be run
#   output = Array that stores output information
#
#   return:
#   
#        0: Test ran successfully
#        !0: Test failed
#------------------------------------------------------------------------------



##
# @fn setFuseConfig()
#
# The same tests are run for kernel mod (kmod) and fuse testing. This function 
# sets the variable to fuse mode.


def setFuseConfig():

    global header 
    global prefix
    global mount_fs
    global run_client
    global mount_as_fuse
    
    header = "OFS VFS benchmarks(fuse)"
    prefix = "vfs-bench-fuse"
    mount_fs = True
    run_client = False
    mount_as_fuse = True
    

##
# @fn setKmodConfig()
#
# The same tests are run for kernel mod (kmod) and fuse testing. This function 
# sets the variable to Kmod mode.


def setKmodConfig():

    global header 
    global prefix
    global mount_fs
    global run_client
    global mount_as_fuse

    header = "OFS VFS benchmarks(kmod)"
    prefix = "vfs-bench-kmod"
    mount_fs = True
    run_client = True
    mount_as_fuse = False



##
#
# @fn bonnie(testing_node,output=[]):
#
# Bonnie++ tests large file IO and creation/deletion of small files.
#
# See http://sourceforge.net/projects/bonnie/
#
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#


def bonnie(testing_node,output=[]):

    
    rc = 0
    #make sure that the benchmarks have been installed
    if testing_node.ofs_extra_tests_location == "":
        testing_node.installBenchmarks()
    
    testing_node.changeDirectory("%s/bonnie++-1.03e" % testing_node.ofs_extra_tests_location)
    
    # check to see if we have already compiled bonnie++
    if testing_node.runSingleCommand( "[ -f %s/bonnie++-1.03e/bonnie++ ]" % testing_node.ofs_extra_tests_location):

        rc = testing_node.runSingleCommand("./configure",output)
        if rc != 0:
            return rc
        rc = testing_node.runSingleCommand("make",output)
        if rc != 0:
            return rc
        
    testing_node.changeDirectory(testing_node.ofs_mount_point)
    rc = testing_node.runSingleCommand(testing_node.ofs_extra_tests_location+"/bonnie++-1.03e/bonnie++  -n 4:1:1:1  -r 16 -s 1024 ",output)
    print output[1]
    print output[2]
    

    return rc

##
#
# @fn dbench(testing_node,output=[]):
#
#   DBENCH is a tool to generate I/O workloads to either a filesystem or to a 
#   networked CIFS or NFS server. It can even talk to an OrangeFS target.
#   DBENCH can be used to stress a filesystem or a server to see which workload
#   it becomes saturated and can also be used for preditcion analysis to 
#   determine "How many concurrent clients/applications performing this 
#   workload can my server handle before response starts to lag?"
#
#   http://dbench.samba.org/
#
#
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
    
def dbench(testing_node,output=[]):
    
    rc = 0
    #make sure that the benchmarks have been installed
    if testing_node.ofs_extra_tests_location == "":
        testing_node.installBenchmarks()
    
    #testing_node.runSingleCommand("mkdir -p %s/dbench-3.03" % (testing_node.ofs_extra_tests_location))
    testing_node.changeDirectory("%s/dbench-3.03" % testing_node.ofs_extra_tests_location)
    
    # check to see if we have already compiled dbench
    if testing_node.runSingleCommand( "[ -f %s/dbench-3.03/dbench ]" % testing_node.ofs_extra_tests_location):

        rc = testing_node.runSingleCommand("make clean",output)
        rc = testing_node.runSingleCommand("./configure",output)

        # Patch dbench to add support for OrangeFS
        rc = testing_node.runSingleCommand("patch -p3 < %s/test/automated/vfs-tests.d/dbench.patch" % testing_node.ofs_source_location,output)
        if rc != 0:
            return rc
        
        rc = testing_node.runSingleCommand("make",output)
        if rc != 0:
            return rc

    # Copy the loadfile to the OrangeFS 
    rc = testing_node.runSingleCommand("cp client.txt %s" % testing_node.ofs_mount_point,output)
    if rc != 0:
        return rc
    
    # Run dbench from the mount_point.
    testing_node.changeDirectory(testing_node.ofs_mount_point)
    
    
    rc = testing_node.runSingleCommand(testing_node.ofs_extra_tests_location+"/dbench-3.03/dbench -c client.txt 100 -t 300 ",output)
    print output[1]
    print output[2]
    

    return rc

##
#
# @fn fdtree(testing_node,output=[]):
#
#   The fdtree software is used for testing the metadata performance of a file 
#   system.
#
#   https://computing.llnl.gov/?set=code&page=sio_downloads
#
#
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#    

def fdtree(testing_node,output=[]):

    
    rc = 0
    #make sure that the benchmarks have been installed
    if testing_node.ofs_extra_tests_location == "":
        testing_node.installBenchmarks()
    
    # Run fdtree from the mount_point
    testing_node.changeDirectory(testing_node.ofs_mount_point)
    rc = testing_node.runSingleCommand(testing_node.ofs_extra_tests_location+"/fdtree-1.0.1/fdtree.bash -l 4 -d 5",output)
    print output[1]
    print output[2]

    
    return rc



##
#
# @fn iozone(testing_node,output=[]):
#
#   IOzone is a filesystem benchmark tool. The benchmark generates and measures
#   a variety of file operations. Iozone has been ported to many machines and 
#   runs under many operating systems.
#
#   Iozone is useful for performing a broad filesystem analysis of a vendor's 
#   computer platform. The benchmark tests file I/O performance for the 
#   following operations:
#
#   Read, write, re-read, re-write, read backwards, read strided, fread, 
#   fwrite, random read, pread ,mmap, aio_read, aio_write
#
#   http://www.iozone.org/
#
#
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#

def iozone(testing_node,output=[]):
    
    rc = 0
    #make sure that the benchmarks have been installed
    if testing_node.ofs_extra_tests_location == "":
        testing_node.installBenchmarks()
    testing_node.changeDirectory("%s/iozone3_239/src/current" % testing_node.ofs_extra_tests_location)
   
    # check to see if we have already compiled iozone
    if testing_node.runSingleCommand( "[ -f %s/iozone3_239/src/current/iozone ]" % testing_node.ofs_extra_tests_location):
        rc = testing_node.runSingleCommand("patch -p5 < %s/test/automated/vfs-tests.d/iozone.patch" % testing_node.ofs_source_location,output)
        if rc != 0:
            return rc
        
        rc = testing_node.runSingleCommand("make linux",output)
        if rc != 0:
            return rc
        
    tmp = []
    testing_node.checkMount(mount_point=testing_node.ofs_mount_point,output=tmp)
    
    rc = testing_node.runSingleCommand("./iozone -a -y 4096 -n $((1024*512)) -g $((1024*1024*4)) -f %s/test_iozone_file" % testing_node.ofs_mount_point,output)


    print output[1]
    print output[2]
        
    return rc



def dd(testing_node,output=[]):

    rc = testing_node.runSingleCommand("dd if=/dev/zero of=%s/gigfile bs=16M count=64" % testing_node.ofs_mount_point, output)
    print output[1]
    print output[2]
    
    testing_node.runSingleCommand("rm %s/gigfile" % testing_node.ofs_mount_point)
    return rc

def linux_untar(testing_node,output=[]):
    
    rc = testing_node.runSingleCommand("cd /tmp; wget --quiet https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.1.15.tar.xz", output)
    
    rc = testing_node.runSingleCommand("cd /tmp; unxz linux-4.1.15.tar.xz",output)
    
    ts = datetime.now()
    
    rc = testing_node.runSingleCommandAsRoot("cd %s; tar xf /tmp/linux-4.1.15.tar" % testing_node.ofs_mount_point)
    
    total_time = str(datetime.now()-ts)
    print "Total time to untar Linux 4.1.15 source is %s ms" % total_time
    
    return rc
                                 

tests = [ 

#dd,
fdtree,
iozone,
bonnie,
dbench,
linux_untar

 ]
