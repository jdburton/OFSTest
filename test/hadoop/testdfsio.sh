#!/usr/bin/env bash
set -x
$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/hadoop*test*.jar TestDFSIO -write -nrFiles 10 -fileSize 100 && \
$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/hadoop*test*.jar TestDFSIO -read -nrFiles 10 -fileSize 100 && \
$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/hadoop*test*.jar TestDFSIO -clean