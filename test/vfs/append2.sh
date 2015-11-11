#!/usr/bin/env bash
set -x
# Need
# OFS_EXTRA_TESTS_DIR
# OFS_SRC_DIR
# OFS_MOUNTPOINT
# OFS_INSTALL_DIR

pvfs2_testdir=${OFS_MOUNTPOINT}/append_dir
pvfs2_testfile=${pvfs2_testdir}/append_test2
local_reference=${OFS_INSTALL_DIR}/append_ref2

datagen() {
	for I in `seq 1 25`; do
		echo "line$I"
	done
}

mkdir -p $pvfs2_testdir

datagen > $local_reference
datagen > $pvfs2_testfile
datagen >> $local_reference
datagen >> $pvfs2_testfile

diff -u $local_reference $pvfs2_testfile
