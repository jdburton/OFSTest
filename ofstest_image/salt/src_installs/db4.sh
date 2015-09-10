#!/usr/bin/env bash
#Copyright Omnibond Systems, LLC. All rights reserved.
#
#Terms of Service are located at:
#http://www.cloudycluster.com/termsofservice

set -x
cd /usr/src/db-4.8.30/build_unix
../dist/configure --prefix=/opt/db4
make -j$(nproc)
make install
