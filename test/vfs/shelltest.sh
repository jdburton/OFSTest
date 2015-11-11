#!/usr/bin/env bash
# Need
# OFS_EXTRA_TESTS_DIR
# OFS_SRC_DIR
# OFS_MOUNTPOINT

cd

bash -x ${OFS_SRC_DIR}/test/kernel/linux-2.6/pvfs2-shell-test.sh $OFS_MOUNT_POINT 2>&1