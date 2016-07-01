/home/ubuntu/.bashrc:
  file.prepend:
    - text: 
      - source /etc/profile
 
/etc/profile.d/jdk.sh:
  file.append:
    - text: 
        - export J2SDKDIR=/usr/lib/jvm/java-8-oracle
        - export J2REDIR=/usr/lib/jvm/java-8-oracle/jre
        - export PATH=$PATH:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin
        - export JAVA_HOME=/usr/lib/jvm/java-8-oracle
        - export DERBY_HOME=/usr/lib/jvm/java-8-oracle/db