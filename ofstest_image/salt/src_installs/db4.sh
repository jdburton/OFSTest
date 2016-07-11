#!/usr/bin/env bash

set -x
cd /usr/src/db-4.8.30/build_unix
../dist/configure --prefix=/opt/db4
make -j$(nproc)
make install
