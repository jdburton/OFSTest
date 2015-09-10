#!/usr/bin/env bash
#Copyright Omnibond Systems, LLC. All rights reserved.
#
#Terms of Service are located at:
#http://www.cloudycluster.com/termsofservice

set -x
cd /usr/src/maui-3.3.1
./configure --prefix=/opt/maui --with-pbs=/opt/torque
make -j$(nproc)
make install
