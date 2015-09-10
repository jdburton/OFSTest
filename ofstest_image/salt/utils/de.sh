#!/usr/bin/env bash
#Copyright Omnibond Systems, LLC. All rights reserved.
#
#Terms of Service are located at:
#http://www.cloudycluster.com/termsofservice

set -x
# Arg1: url of file to download and extract
# Arg2: the directory where archive contents will be extracted
cd /tmp && \
wget --no-check-certificate -nv $1 && \
tar -C $2 -xzf $(basename $1)
