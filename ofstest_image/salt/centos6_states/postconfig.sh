#!/bin/bash
set -x
sudo chown -R centos:centos /opt
sudo /sbin/modprobe -v fuse
sudo chmod a+x /bin/fusermount
