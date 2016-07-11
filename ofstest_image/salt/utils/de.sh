#!/usr/bin/env bash

set -x
# Arg1: url of file to download and extract
# Arg2: the directory where archive contents will be extracted
cd /tmp && \
wget --no-check-certificate -nv $1 && \
df -h
tar -C $2 -xzf $(basename $1)
