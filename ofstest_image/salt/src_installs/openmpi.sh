#!/usr/bin/env bash


set -x
cd /opt/mpi/openmpi-1.8.8
./configure --prefix=/opt/mpi/openmpi --enable-shared --with-pic \
  --with-io-romio-flags='--with-pvfs2=/opt/orangefs --with-file-system=pvfs2+nfs+ufs' \
  --with-tm=/opt/torque 
make -j$(nproc) 
make install
export PATH=$PATH:/opt/mpi/openmpi/bin
if which mpicc
then
  cd /opt/mpi/openmpi-1.8.8/ompi/mca/io/romio/romio/test/
  make 
fi