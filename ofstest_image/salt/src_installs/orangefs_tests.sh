#!/bin/bash


set -x

cd /opt/orangefs_src/test


export PATH=$PATH:/opt/mpi/openmpi/bin
CFLAGS='-g -O0' ./configure  --prefix=/opt/orangefs --with-db=/opt/db4 --with-mpi=/opt/mpi/openmpi --enable-strict --enable-shared && \
# kludge because perfbase won't compile.
rm -rf perfbase
make && \
make install


