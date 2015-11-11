#!/usr/bin/env bash
set -x

# Need
# OFS_EXTRA_TESTS_DIR
# OFS_SRC_DIR
# OFS_MOUNTPOINT

cd $OFS_EXTRA_TESTS_DIR/iozone3_239/src/current


if [ ! -f $OFS_EXTRA_TESTS_DIR/iozone3_239/src/current/iozone ]
then
    patch -p5 < $OFS_SRC_DIR/test/automated/vfs-tests.d/iozone.patch
    make linux

fi

./iozone -a -y 4096 -q $((1024*16)) -n 4096 -g $((1024*16*4)) -f $OFS_MOUNTPOINT/test_iozone_file
