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


header = "OFS MPI-VFS Test"
prefix = "mpivfs"
mount_fs = True
run_client = True
mount_as_fuse = False
debug = True

def functions(testing_network):
    pass
def heidleberg_IO(testing_network):
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
    testing_node.changeDirectory("/opt/mpi/%s/ompi/mca/io/romio/romio/test"  % testing_node.openmpi_version)
    
    rc = 0
    print "%s -machinefile=%s -fname=%s/romioruntests" % (testing_node.romio_runtests_pvfs2,testing_node.created_openmpihosts,testing_node.ofs_mount_point)
    rc = testing_node.runSingleCommand("%s -machinefile=%s -fname=%s/romioruntests" % (testing_node.romio_runtests_pvfs2,testing_node.created_openmpihosts,testing_node.ofs_mount_point),output)
    
    #TODO: Compare actual results with expected.
    
    return rc

##
#
# @fn IOR(testing_node,output=[]):
#
# @brief This is the IOR testsuite from LLNL. 
#
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def IOR(testing_node,output=[]):

    rc = testing_node.changeDirectory("/opt/mpi/IOR/src/C")
    np = testing_node.runSingleCommandBacktick("wc -l < testing_node.created_openmpihosts")
    
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 /opt/mpi/IOR/src/C/IOR -a MPIIO -i 4 -N %s -b 2g -t 2m -s 1 -o pvfs2:%s/mpiiofile" % (np,testing_node.openmpi_installation_location,testing_node.created_openmpihosts,np,testing_node.ofs_mount_point),output)
    
    #TODO: Compare actual results with expected.
    
    return rc


tests = [ romio_testsuite, IOR ]



