#!/usr/bin/env bash

set -x


GENSIZE=10000000

$HADOOP_PREFIX/bin/hadoop jar  $HADOOP_PREFIX/hadoop*examples*.jar  teragen $GENSIZE /user/$USER/terasort-${GENSIZE}-input && \
$HADOOP_PREFIX/bin/hadoop jar  $HADOOP_PREFIX/hadoop*examples*.jar  terasort /user/$USER/terasort-${GENSIZE}-input /user/$USER/terasort-${GENSIZE}-output && \
$HADOOP_PREFIX/bin/hadoop jar  $HADOOP_PREFIX/hadoop*examples*.jar  teravalidate $GENSIZE /user/$USER/terasort-${GENSIZE}-output

