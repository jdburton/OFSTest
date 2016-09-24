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
header = "OFS MPI-VFS Test"
prefix = "mpi-benchmarks"
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

def IOR_posix(testing_node,output=[]):

    rc = testing_node.changeDirectory("%s/src/C" % testing_node.ior_installation_location)
    np = testing_node.number_mpi_slots

    bs = 16384 / int(np)
    
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/src/C/IOR -a POSIX -F -i 1 -N %s -b %dm -k -t 4m -s 1 -o %s/mpivfsfile" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.ior_installation_location,np,bs,testing_node.ofs_mount_point),output)
    
    #TODO: Compare actual results with expected.
    time.sleep(30)
    testing_node.runSingleCommand("rm -f /tmp/mount/orangefs/mpivfsfile*")
    print output[1]
    print output[2]
    
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

def IOR_single_posix(testing_node,output=[]):

    rc = testing_node.changeDirectory("%s/src/C" % testing_node.ior_installation_location)
    np = testing_node.number_mpi_hosts

    bs = 16384 / int(np)
    
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/src/C/IOR -a POSIX -F -i 1 -N %s -b %dm -t 4m -s 1 -o %s/mpivfsfile" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.ior_installation_location,np,bs,testing_node.ofs_mount_point),output)
    
    #TODO: Compare actual results with expected.
    time.sleep(30)
    testing_node.runSingleCommand("rm -f /tmp/mount/orangefs/mpivfsfile*")
    print output[1]
    print output[2]

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

def IOR_single_mpiio(testing_node,output=[]):

    rc = testing_node.changeDirectory("%s/src/C" % testing_node.ior_installation_location)
    np = testing_node.number_mpi_hosts
    
    bs = 16384 / int(np)
    
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/src/C/IOR -a MPIIO -C -i 1 -N %s -b %dm -t 4m -s 1 -o pvfs2:%s/mpiiofile" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.ior_installation_location,np,bs,testing_node.ofs_mount_point),output)
    time.sleep(30)
    print output[1]
    print output[2]
    
    
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

def IOR_mpiio(testing_node,output=[]):

    rc = testing_node.changeDirectory("%s/src/C" % testing_node.ior_installation_location)
    np = testing_node.number_mpi_slots
    bs = 16384 / int(np)
    
    
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/src/C/IOR -a MPIIO -C -i 1 -N %s -b %dm -k -t 4m -s 1 -o pvfs2:%s/mpiiofile" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.ior_installation_location,np,bs,testing_node.ofs_mount_point),output)
    time.sleep(30)
    print output[1]
    print output[2]
    
    
    
    return rc

##
#
# @fn mdtest(testing_node,output=[]):
#
# @brief This is the mdtest testsuite from LLNL. 
#
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def mdtest(testing_node,output=[]):

    rc = testing_node.changeDirectory(testing_node.mdtest_installation_location)
    np = testing_node.number_mpi_slots
    
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/mdtest  -n 256 -w 4194304 -i 1 -d %s/mdtest" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.mdtest_installation_location,testing_node.ofs_mount_point),output)
    
    #TODO: Compare actual results with expected.
    time.sleep(30)
    print output[1]
    print output[2]

    return rc


##
#
# @fn simul(testing_node,output=[]):
#
# @brief This is the simul testsuite from LLNL. 
#
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def simul(testing_node,output=[]):

    rc = testing_node.changeDirectory(testing_node.mdtest_installation_location)
    np = testing_node.number_mpi_slots
    
    #skip tests 18,38,39. OrangeFS does not support hard links.
    rc = testing_node.runSingleCommand("mkdir -p %s/simul" % testing_node.ofs_mount_point)
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/simul -e 18,38,39 -v -d %s/simul" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.simul_installation_location,testing_node.ofs_mount_point),output)
    
    #TODO: Compare actual results with expected.
    # Wait for all changes to be written.
    time.sleep(30)
    print output[1]
    print output[2]

    
    return rc



##
#
# @fn multi_md_test(testing_node,output=[]):
#
# @brief This is the OrangeFS multi_md_test 
#
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def multi_md_test(testing_node,output=[]):

    
    np = testing_node.number_mpi_slots
    
    rc = testing_node.changeDirectory(testing_node.ofs_mount_point)
    testing_node.runSingleCommand("mkdir -p %s/multi_md_test" % testing_node.ofs_mount_point)
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/test/multi-md-test -d %s/multi_md_test -n 100 -s 1024 -a 0 -p 5 -c 1,1,%s" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.ofs_installation_location,testing_node.ofs_mount_point,np),output)
    
    #TODO: Compare actual results with expected.
    time.sleep(30)
    print output[1]
    print output[2]

    return rc


##
#
# @fn multi_md_test(testing_node,output=[]):
#
# @brief This is the OrangeFS multi_md_test 
#
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def multi_md_test_size_sweep(testing_node,output=[]):

    
    np = testing_node.number_mpi_slots
    
    rc = testing_node.changeDirectory(testing_node.ofs_mount_point)
    testing_node.runSingleCommand("mkdir -p %s/multi_md_size_sweep" % testing_node.ofs_mount_point)
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/test/multi-md-test-size-sweep -d %s/multi_md_size_sweep -n 1000 -a 0 -s 1,1,%s" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.ofs_installation_location,testing_node.ofs_mount_point,np),output)
    
    #TODO: Compare actual results with expected.
    time.sleep(30)
    print output[1]
    print output[2]

    return rc

##
#
# @fn mpi_md_test(testing_node,output=[]):
#
# @brief This is the mpi_md_test.
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#
def mpi_md_test(testing_node,output=[]):

    rc = mpi_md_test_create(testing_node,output)
    if rc:
        print "mpi_md_test create failed with rc = %r" % rc
        return rc

    rc = mpi_md_test_resize(testing_node,output)
    if rc:
        print "mpi_md_test resize failed with rc = %r" % rc
        return rc

    rc = mpi_md_test_delete(testing_node,output)
    if rc:
        print "mpi_md_test delete failed with rc = %r" % rc

    return rc


def mpi_md_test_create(testing_node,output=[]):

    #/opt/mpi/openmpi-1.6.5/ompi/mca/io/romio/romio/test
    
    rc = testing_node.changeDirectory("%s" % testing_node.ofs_mount_point)
    np = testing_node.number_mpi_slots
    testing_node.runSingleCommand("mkdir -p %s/mpi_md_test" % testing_node.ofs_mount_point)
    time.sleep(5)
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/test/mpi-md-test -O -n 100 -d pvfs2:%s/mpi_md_test" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.ofs_installation_location,testing_node.ofs_mount_point),output)

    print output[1]
    print output[2]
    
    time.sleep(30)
    #TODO: Compare actual results with expected.
    
    return rc

def mpi_md_test_resize(testing_node,output=[]):

    #/opt/mpi/openmpi-1.6.5/ompi/mca/io/romio/romio/test

    rc = testing_node.changeDirectory("%s" % testing_node.ofs_mount_point)
    np = testing_node.number_mpi_slots

    time.sleep(5)
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/test/mpi-md-test -R -n 100 -d pvfs2:%s/mpi_md_test" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.ofs_installation_location,testing_node.ofs_mount_point),output)

    print output[1]
    print output[2]

    time.sleep(30)
    #TODO: Compare actual results with expected.

    return rc

def mpi_md_test_delete(testing_node,output=[]):

    #/opt/mpi/openmpi-1.6.5/ompi/mca/io/romio/romio/test

    rc = testing_node.changeDirectory("%s" % testing_node.ofs_mount_point)
    np = testing_node.number_mpi_slots
    time.sleep(5)
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/test/mpi-md-test -D -n 100 -d pvfs2:%s/mpi_md_test" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.ofs_installation_location,testing_node.ofs_mount_point),output)

    print output[1]
    print output[2]

    time.sleep(30)
    #TODO: Compare actual results with expected.

    return rc

##
#
# @fn mpi_unbalanced_test(testing_node,output=[]):
#
# @brief This is the mpi_unbalanced_test.
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def mpi_unbalanced_test(testing_node,output=[]):

    #/opt/mpi/openmpi-1.6.5/ompi/mca/io/romio/romio/test
    
    rc = testing_node.changeDirectory("%s" % testing_node.ofs_mount_point)
    np = testing_node.number_mpi_slots
    testing_node.runSingleCommand("mkdir -p %s/mpi_unbalanced_test" % testing_node.ofs_mount_point)
    time.sleep(5)
    rc = testing_node.runSingleCommand("time %s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/test/mpi-unbalanced-test pvfs2:%s/mpi_unbalanced_test > /dev/null" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.ofs_installation_location,testing_node.ofs_mount_point),output)
    
    time.sleep(30)
    #TODO: Compare actual results with expected.
    print output[1]
    print output[2]

    
    return rc

##
#
# @fn mpi_tile_io(testing_node,output=[]):
#
# @brief This is the mpi_tile_io test test.
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def mpi_tile_io(testing_node,output=[]):

    #/opt/mpi/openmpi-1.6.5/ompi/mca/io/romio/romio/test
    
    rc = testing_node.changeDirectory("%s" % testing_node.ofs_mount_point)
    np = testing_node.number_mpi_slots
    testing_node.runSingleCommand("mkdir -p %s/mpi_tile_io" % testing_node.ofs_mount_point)
    testing_node.runSingleCommand("touch %s/mpi_tile_io/tilefile" % testing_node.ofs_mount_point)
    
    tiles_y = 1
    if (int(np) > 1):
        tiles_y =  int(np)/2
    
    time.sleep(5)
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %s --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/mpi-tile-io --nr_tiles_x 2 --nr_tiles_y %d --sz_tile_x 1000 --sz_tile_y 1000 --sz_element 2048 --filename %s/mpi_tile_io/tilefile --collective" % (testing_node.openmpi_installation_location,np,testing_node.created_openmpihosts,testing_node.mpi_tile_io_installation_location,tiles_y,testing_node.ofs_mount_point),output)
    
    time.sleep(30)
    #TODO: Compare actual results with expected.
    print output[1]
    print output[2]

    
    return rc


##
#
# @fn npb_mpi(testing_node,output=[]):
#
# @brief This is the mpi part of the NPB test.
# @param testing_node OFSTestNode on which tests are run.
# @param output Array that holds output from commands. Passed by reference. 
#   
# @return 0 Test ran successfully
# @return Not 0 Test failed
#
#

def npb_mpi(testing_node,output=[]):

    #/opt/mpi/openmpi-1.6.5/ompi/mca/io/romio/romio/test
    
    rc = testing_node.changeDirectory("%s" % testing_node.ofs_mount_point)
    np = testing_node.number_mpi_slots
    testing_node.runSingleCommand("mkdir -p %s/npb_mpi" % testing_node.ofs_mount_point)
    testing_node.runSingleCommand("cp %s/BT/inputbt.data.sample %s/npb_mpi/inputbt.data" % (testing_node.npb_mpi_installation_location,testing_node.ofs_mount_point))
    
    sq_np = 1
    if (int(np) >= 4):
        sq_np = 4
    if (int(np) >= 9):
        sq_np = 9
    if (int(np) >= 16):
        sq_np = 16
     
    
    time.sleep(5)
    rc = testing_node.runSingleCommand("%s/bin/mpiexec -np %d --machinefile %s --map-by node --mca btl_tcp_if_include eth0 %s/bin/bt.C.4.mpi_io_full" % (testing_node.openmpi_installation_location,sq_np,testing_node.created_openmpihosts,testing_node.npb_mpi_installation_location),output)
    
    time.sleep(30)
    #TODO: Compare actual results with expected.
    print output[1]
    print output[2]

    
    return rc


tests = [
         mdtest,
         mpi_md_test,
         multi_md_test,
         multi_md_test_size_sweep,
         mpi_unbalanced_test,

         IOR_single_posix,
         IOR_single_mpiio,
         IOR_posix,
         IOR_mpiio,
         npb_mpi,
         mpi_tile_io       
         
          ]




