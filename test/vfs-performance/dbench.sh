#!/usr/bin/env bash
set -x
# Need
# OFS_EXTRA_TESTS_DIR
# OFS_SRC_DIR
# OFS_MOUNTPOINT

cd $OFS_EXTRA_TESTS_DIR/dbench-3.03

# check to see if we have already compiled dbench
if [ ! -f $OFS_EXTRA_TESTS_DIR/dbench-3.03/dbench ]
then
    make clean
    ./configure
    patch -p3 < $OFS_SRC_DIR/test/automated/vfs-tests.d/dbench.patch
    make
fi

cp client.txt $OFS_MOUNTPOINT

cd $OFS_MOUNTPOINT

$OFS_EXTRA_TESTS_DIR/dbench-3.03/dbench -c client.txt 100 -t 300
