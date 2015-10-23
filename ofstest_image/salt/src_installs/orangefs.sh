#!/bin/bash


set -x

mkdir -p /opt/orangefs

whoami

svn co http://www.orangefs.org/svn/orangefs/trunk /opt/orangefs_src
cd /opt/orangefs_src
./prepare

if sudo /sbin/modprobe -v orangefs
then
    ./configure  --prefix=/opt/orangefs --with-db=/opt/db4 --enable-strict --enable-shared --enable-fuse && \
    make && \
    make install
else
    ./configure  --prefix=/opt/orangefs --with-db=/opt/db4 --with-kernel=/lib/modules/`uname -r`/build --enable-strict --enable-shared --enable-fuse && \
    make && \
    make install && \
    make kmod && \
    sudo make kmod_install

fi

