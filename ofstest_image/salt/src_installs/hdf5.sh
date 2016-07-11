#!/usr/bin/env bash

set -x
cd /usr/src/hdf5*
./configure --enable-parallel --prefix=/opt/hdf5 --enable-fortran
make -j$(nproc)
make install