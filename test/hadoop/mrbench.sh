#!/usr/bin/env bash
set -x
$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/hadoop*test*.jar mrbench -numRuns 50