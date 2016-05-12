#!/usr/bin/env bash
set -x
# Need
# OFS_EXTRA_TESTS_DIR
# OFS_SRC_DIR
# OFS_MOUNTPOINT



LTP_ARCHIVE_VERSION="20160510"
LTP_ARCHIVE_TYPE=".tar.gz"
LTP_ARCHIVE=${LTP_ARCHIVE_VERSION}${LTP_ARCHIVE_TYPE}
LTP_PREFIX="/opt/ltp"
LTP_URL="https://github.com/linux-test-project/ltp/archive"


cd $OFS_EXTRA_TESTS_DIR

if [ ! -f ${LTP_PREFIX}/runltp ]
then
    rm -rf ltp-${LTP_ARCHIVE_VERSION}*
    wget --no-check-certificate --output-document=${LTP_ARCHIVE} ${LTP_URL}/${LTP_ARCHIVE}
    tar zxf $LTP_ARCHIVE
    cd ltp-${LTP_ARCHIVE_VERSION}
    patch -p1 < ${OFS_SRC_DIR}/test/automated/vfs-tests.d/ltp-${LTP_ARCHIVE_VERSION}-zoo-path.patch
    make autotools
    DEBUG_CFLAGS='-g' OPT_CFLAGS='-O0' ./configure --prefix=${LTP_PREFIX}
    make all
    make install

fi


cp ${OFS_SRC_DIR}/test/automated/vfs-tests.d/ltp-pvfs-testcases ${LTP_PREFIX}/runtest/
mkdir -p ${OFS_MOUNTPOINT}/ltp-tmp
chmod 777 ${OFS_MOUNTPOINT}/ltp-tmp
umask 0

cd LTP_PREFIX


#print 'sudo PVFS2TAB_FILE=%s/etc/orangefstab LD_LIBRARY_PATH=/opt/db4/lib:%s/lib64:%s/lib ./runltp -p -l %s/ltp-pvfs-testcases-%s.log -d %s/ltp-tmp -f ltp-pvfs-testcases -A %s/zoo.tmp 2>&1 | tee %s/ltp-pvfs-testcases-%s.output' % (testing_node.ofs_installation_location,testing_node.ofs_installation_location,testing_node.ofs_installation_location,testing_node.ofs_installation_location, vfs_type, testing_node.ofs_mount_point,testing_node.ofs_extra_tests_location,testing_node.ofs_installation_location,vfs_type)
sudo -E ./runltp -p -l ${OFS_INSTALL_DIR}/ltp-pvfs-testcases-vfs.log -d ${OFS_MOUNTPOINT}/ltp-tmp -f ltp-pvfs-testcases -A ${OFS_EXTRA_TESTS_DIR}/zoo.tmp 2>&1 | tee ${OFS_INSTALL_DIR}/ltp-pvfs-testcases-vfs.output

    # check to see if log file is there
if [ ! -f ${OFS_INSTALL_DIR}/ltp-pvfs-testcases-vfs.log ]
then
    echo "Could not find ltp-pvfs-testcases.log file."
    exit 1
fi

# Look to see if any tests failed.
! grep TFAIL ${OFS_INSTALL_DIR}/ltp-pvfs-testcases-vfs.log






