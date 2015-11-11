#!/usr/bin/env bash
set -x
# Requires:
#  HADOOP_PREFIX

mkdir -p $HOME/gutenberg
cd $HOME/gutenberg
$HADOOP_PREFIX/bin/hadoop dfs -mkdir -p /user/$USER/gutenberg

    # get the gutenberg files
wget http://www.gutenberg.org/cache/epub/5000/pg5000.txt
wget http://www.gutenberg.org/cache/epub/20417/pg20417.txt
wget http://www.gutenberg.org/cache/epub/4300/pg4300.txt

$HADOOP_PREFIX/bin/hadoop dfs -copyFromLocal $HOME/gutenberg/* /user/$USER/gutenberg && \
$HADOOP_PREFIX/bin/hadoop jar  $HADOOP_PREFIX/hadoop*examples*.jar wordcount /user/$USER/gutenberg /user/$USER/gutenberg-output

