#!/usr/bin/env bash
set -x
# Need
# OFS_EXTRA_TESTS_DIR
# OFS_SRC_DIR
# OFS_MOUNTPOINT
# URL_BASE
# OFS_PORT

# Should move to provisioning.
cd
git clone git://oss.sgi.com/xfs/cmds/xfstests

cd ./xfstests
wget ${URL_BASE}/xfstests-pvfs2.diff
patch -p1 < xfstests-pvfs2.diff
make
wget ${URL_BASE}/xfstests-exclude.list
# ---

sudo TEST_DIR=${OFS_MOUNT_POINT} TEST_DEV=tcp://`hostname`:${OFS_PORT}/orangefs ./check -pvfs2 -E xfstests-exclude.list
