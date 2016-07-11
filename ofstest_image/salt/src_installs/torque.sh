#!/usr/bin/env bash

set -x
cd /usr/src/torque-5.0.1-1_4fa836f5
./configure --prefix=/opt/torque
make -j$(nproc)
make install
