/etc/profile.d/java.sh:
  file.append:
    - text: export JAVA_HOME=/usr/lib/jvm/java-7-oracle
    
/home/ubuntu/.bashrc:
  file.prepend:
    - text: 
      - \#!/bin/bash
      - source /etc/profile
 