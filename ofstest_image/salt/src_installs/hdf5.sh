#!/usr/bin/env bash
#Copyright Omnibond Systems, LLC. All rights reserved.
#
#Terms of Service are located at:
#http://www.cloudycluster.com/termsofservice

set -x
cd /usr/src/hdf5*
./configure --enable-parallel --prefix=/opt/hdf5 --enable-fortran
make -j$(nproc)
make install