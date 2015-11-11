#!/usr/bin/env bash
set -x

# Need
# OFS_EXTRA_TESTS_DIR
# OFS_MOUNTPOINT


cd $OFS_EXTRA_TESTS_DIR/bonnie++-1.03e

# check to see if we have already compiled bonnie++

if [ ! -f $OFS_EXTRA_TESTS_DIR/bonnie++-1.03e/bonnie++ ]
then
    make clean
    ./configure
    make
fi

cd $OFS_MOUNTPOINT

$OFS_EXTRA_TESTS_DIR/bonnie++-1.03e/bonnie++ -n 4:1:1:1  -r 16 -s 1024