#!/bin/bash


set -x

mkdir -p /opt/orangefs

whoami

svn co http://dev.orangefs.org/svn/orangefs/trunk /opt/orangefs_src
cd /opt/orangefs_src
./prepare


./configure  --with-db-backend=bdb --prefix=/opt/orangefs --with-db=/opt/db4 --enable-strict --enable-shared --enable-fuse && \
make && \
make install

