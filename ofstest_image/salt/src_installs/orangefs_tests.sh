#!/bin/bash


set -x

cd /opt/orangefs_src/test


export PATH=$PATH:/opt/mpi/openmpi-1.8.8/bin
CFLAGS='-g -O0' ./configure  --with-db-backend=bdb --prefix=/opt/orangefs --with-db=/opt/db4 --with-mpi=/opt/mpi/openmpi-1.8.8 --enable-strict --enable-shared && \
# kludge because perfbase won't compile.
rm -rf perfbase
rm -rf io
make && \
make install


