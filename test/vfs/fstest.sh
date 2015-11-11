#!/usr/bin/env bash
set -x
# Need
# OFS_EXTRA_TESTS_DIR
# OFS_SRC_DIR
# OFS_MOUNTPOINT

mkdir -p ${OFS_MOUNTPOINT}/fstest

if [ ! -f $OFS_SRC_DIR/fstest ]
then
    gcc $OFS_SRC_DIR/test/automated/vfs-tests.d/fstest.c -o $OFS_SRC_DIR/fstest
fi

$OFS_SRC_DIR/fstest -p $OFS_MOUNTPOINT/fstest