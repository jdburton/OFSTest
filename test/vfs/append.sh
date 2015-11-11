#!/usr/bin/env bash
set -x
# Need
# OFS_EXTRA_TESTS_DIR
# OFS_SRC_DIR
# OFS_INSTALL_DIR
# OFS_MOUNTPOINT


pvfs2_testfile=${OFS_MOUNTPOINT}/append_test
local_reference=${OFS_INSTALL_DIR}/append_ref
datagen() {
	for I in `seq 1 25`; do
		echo "line$I"
	done
}

datagen > $local_reference
datagen > $pvfs2_testfile
datagen >> $local_reference
datagen >> $pvfs2_testfile

diff -u $local_reference $pvfs2_testfile
