#!/usr/bin/env bash
set -x

# Need
# OFS_SRC_DIR
# OFS_MOUNTPOINT

mkdir -p $OFS_MOUNTPOINT/fsx

if [ ! -f %s/fsx ]
then
    gcc $OFS_SRC_DIR/test/automated/vfs-tests.d/fsx.c -o $OFS_MOUNTPOINT/fsx
fi

$OFS_SRC_DIR/fsx -N 1000 -W -R $OFS_MOUNT_POINT/fsx_testfile
