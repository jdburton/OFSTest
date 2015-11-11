#!/bin/bash


set -x

mkdir -p /opt/orangefs

whoami

svn co http://www.orangefs.org/svn/orangefs/trunk /opt/orangefs_src
cd /opt/orangefs_src
./prepare


./configure  --prefix=/opt/orangefs --with-db=/opt/db4 --enable-strict --enable-shared --enable-fuse && \
make && \
make install

