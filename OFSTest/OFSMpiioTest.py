#!/usr/bin/python
##
#
# @namespace OFSMpiioTest
#
# @brief This class implements mpi-io tests to be run on the virtual file system.
#
#
# @var  header 
# Name of header printed in output file
# @var  prefix  
# Name of prefix for test name
# @var  run_client  
# False
# @var  mount_fs  
# Does the file system need to be mounted?
# @var  mount_as_fuse
# Do we mount it via fuse?
# @var  tests  
# List of test functions (at end of file)
#
#

import time
header = "OFS MPI-IO Test"
prefix = "mpiio"
mount_fs = False
run_client = False
mount_as_fuse = False
debug = True

def functions(testing_network):
    pass

def ior_mpiio(testing_network):
    pass
def ior_mpiio_3(testing_network):
    pass
def noncontig(testing_network):
    pass
def romio_async(testing_network):
    pass
def romio_coll_test(testing_network):
    pass
def romio_error(testing_network):
    pass
def romio_excl(testing_network):
    pass
def romio_file_info(testing_network):
    pass
def romio_noncontig_coll2(testing_network):
    pass
def romio_psimple(testing_network):
    pass
def romio_simple(testing_network):
    pass
def romio_split_coll(testing_network):
    pass
def romio_status(testing_network):
    pass
def stadler_file_view_test(testing_network):
    pass
    
##
#
# @fn romio_testsuite(testing_node,output=[]):
#
# @brief This is the romio testsuite that comes with mpich and can also be used with OpenMPI. 
# This does not use pbs/torque, but uses the MPI process managers directly.
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def romio_testsuite(testing_node,output=[]):

    #/opt/mpi/openmpi-1.6.5/ompi/mca/io/romio/romio/test
    testing_node.changeDirectory("/opt/mpi/%s/ompi/mca/io/romio/romio/test" % testing_node.openmpi_version)
    
    rc = 0
    print "%s -machinefile=%s -fname=pvfs2:%s/romioruntests" % (testing_node.romio_runtests_pvfs2,testing_node.created_openmpihosts,testing_node.ofs_mount_point)
    rc = testing_node.runSingleCommand("%s -machinefile=%s -fname=pvfs2:%s/romioruntests" % (testing_node.romio_runtests_pvfs2,testing_node.created_openmpihosts,testing_node.ofs_mount_point),output)
    
    #TODO: Compare actual results with expected.
    time.sleep(30)
    return rc



##
#
# @fn heidelberg_IO(testing_node,output=[]):
#
# @brief This is the heidelberg_IO test.
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def heidelberg_IO(testing_node,output=[]):

    #/opt/mpi/openmpi-1.6.5/ompi/mca/io/romio/romio/test
    
    rc = testing_node.changeDirectory("%s" % testing_node.heidelberg_installation_location)
    np = testing_node.number_mpi_slots
    
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --prefix %s --map-by node %s/heidelberg-IO pvfs2:%s/heidelberg-io-test level0 level1 level2 level3" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.openmpi_installation_location,testing_node.heidelberg_installation_location,testing_node.ofs_mount_point),output)

    print output[1]
    print output[2]

    
    time.sleep(30)
    #TODO: Compare actual results with expected.
    
    return rc


##
#
# @fn mpi_io_test(testing_node,output=[]):
#
# @brief This is the mpi_io_test.
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def mpi_io_test(testing_node,output=[]):

    #/opt/mpi/openmpi-1.6.5/ompi/mca/io/romio/romio/test
    
    rc = testing_node.changeDirectory("%s" % testing_node.ofs_mount_point)
    np = testing_node.number_mpi_slots
    
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --prefix %s --map-by node %s/test/mpi-io-test -f pvfs2:%s/mpi-io-test -b $((1024*1024*32))" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.openmpi_installation_location,testing_node.ofs_installation_location,testing_node.ofs_mount_point),output)
    
    time.sleep(30)
    #TODO: Compare actual results with expected.

    print output[1]
    print output[2]
    
    return rc


##
#
# @fn mpi_io_test_collective(testing_node,output=[]):
#
# @brief This is the mpi_io_test.
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def mpi_io_test_collective(testing_node,output=[]):

    #/opt/mpi/openmpi-1.6.5/ompi/mca/io/romio/romio/test
    
    rc = testing_node.changeDirectory("%s" % testing_node.ofs_mount_point)
    np = testing_node.number_mpi_slots
    
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --prefix %s --map-by node %s/test/mpi-io-test -f pvfs2:%s/mpi-io-test-C -b $((1024*1024*32)) -C" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.openmpi_installation_location,testing_node.ofs_installation_location,testing_node.ofs_mount_point),output)
    
    time.sleep(30)

    print output[1]
    print output[2]

    
    #TODO: Compare actual results with expected.
    
    return rc





##
#
# @fn stadler(testing_node,output=[]):
#
# @brief This is the stadler test.
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def stadler(testing_node,output=[]):

    # Stadler dumps core for some reason. 
    #/opt/mpi/openmpi-1.6.5/ompi/mca/io/romio/romio/test
    
    rc = testing_node.changeDirectory("%s" % testing_node.stadler_installation_location)
    np = testing_node.number_mpi_slots
    
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --prefix %s --map-by node %s/stadler-file-view-test pvfs2:%s/stadler-file-view-test " % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.openmpi_installation_location,testing_node.stadler_installation_location,testing_node.ofs_mount_point),output)
    
    
    #TODO: Compare actual results with expected.
    time.sleep(30)
    
    print output[1]
    print output[2]

    return rc



tests = [ romio_testsuite,
         mpi_io_test,
         mpi_io_test_collective,
         #IOR_single, 
         heidelberg_IO

         #stadler 
         ]



