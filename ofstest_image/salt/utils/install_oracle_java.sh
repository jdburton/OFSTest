#!/bin/bash

# install Sun Java7 for hadoop via webupd8. Fallback to OpenJDK.
add-apt-repository ppa:webupd8team/java < /dev/null
apt-get update
bash -c 'echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections'
bash -c 'echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections'
DEBIAN_FRONTEND=noninteractive apt-get install -y -q oracle-java8-installer || apt-get install -y openjdk-8-jre openjdk-8-jre-lib
                