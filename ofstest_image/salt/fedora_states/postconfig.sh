#!/bin/bash
set -x
sudo chown -R fedora:fedora /opt
sudo /sbin/modprobe -v fuse
sudo chmod a+x /bin/fusermount
