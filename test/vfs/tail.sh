#!/usr/bin/env bash
set -x
# Need
# OFS_EXTRA_TESTS_DIR
# OFS_SRC_DIR
# OFS_INSTALL_DIR
# OFS_MOUNTPOINT



tail_file=${OFS_MOUNTPOINT}/tail_file
tail_output=${OFS_MOUNTPOINT}/tail_output_vfs
local_file=${OFS_INSTALL_DIR}/tail_file
local_output=${OFS_INSTALL_DIR}/tail_output_vfs

datagen() {
	for I in `seq 1 25`; do
		echo "line$I"
	done
}

datagen > $tail_file
datagen > $local_file

tail $tail_file > $tail_output
tail $local_file > $local_output

diff $tail_output $local_output



