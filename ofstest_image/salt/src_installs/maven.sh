#!/usr/bin/env bash
#Copyright Omnibond Systems, LLC. All rights reserved.
#
#Terms of Service are located at:
#http://www.cloudycluster.com/termsofservice

set -x
# Check to see if the package manager has already installed maven.
ln -s /opt/maven /opt/apache-maven-3.2.5
if ! which mvn
then	
   	ln -s /opt/apache-maven-3.2.5/bin/mvn /usr/bin/mvn
fi

