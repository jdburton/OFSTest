#!/usr/bin/env bash
#Copyright Omnibond Systems, LLC. All rights reserved.
#
#Terms of Service are located at:
#http://www.cloudycluster.com/termsofservice

set -x
cd /opt/mpi/openmpi-1.8.8
./configure --prefix=/opt/mpi/openmpi --enable-shared --with-pic \
  --with-io-romio-flags='--with-pvfs2=/opt/orangefs --with-file-system=pvfs2+nfs' \
  --with-tm=/opt/torque
make -j$(nproc)
make install
#cd /opt/mpi/openmpi-1.8.8/ompi/mca/io/romio/romio/test/
#make
