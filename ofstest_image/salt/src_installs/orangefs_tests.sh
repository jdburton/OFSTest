#!/bin/bash


set -x

cd ~/orangefs_src/test
# kludge because perfbase won't compile.
rm -rf perfbase

export PATH=$PATH:/opt/mpi/openmpi/bin
CFLAGS='-g -O0' ./configure  --prefix=/opt/orangefs --with-db=/opt/db4 --with-mpi=/opt/mpi/openmpi --enable-strict --enable-shared && \
make && \
make install


