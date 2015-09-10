#!/usr/bin/env bash
#Copyright Omnibond Systems, LLC. All rights reserved.
#
#Terms of Service are located at:
#http://www.cloudycluster.com/termsofservice

set -x
cd /usr/src/torque-5.0.1-1_4fa836f5
./configure --prefix=/opt/torque
make -j$(nproc)
make install
