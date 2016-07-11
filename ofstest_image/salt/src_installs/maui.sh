#!/usr/bin/env bash

set -x
cd /usr/src/maui-3.3.1
./configure --prefix=/opt/maui --with-pbs=/opt/torque
make -j$(nproc)
make install
