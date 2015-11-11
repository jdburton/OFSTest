#!/usr/bin/env bash
set -x

# Need
# OFS_EXTRA_TESTS_DIR
# OFS_MOUNTPOINT


cd $OFS_MOUNTPOINT
$OFS_EXTRA_TESTS_DIR/fdtree-1.0.1/fdtree.bash -l 4 -d 5