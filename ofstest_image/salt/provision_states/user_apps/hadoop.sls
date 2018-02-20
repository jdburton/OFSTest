hadoop_de:
  cmd.script:
    - source: salt://utils/de.sh
    - args: "http://www.us.apache.org/dist/hadoop/common/hadoop-2.9.0/hadoop-2.9.0.tar.gz /opt/"
    - creates: /opt/hadoop-2.9.0/
  file.directory:
    - name: /opt/hadoop-2.9.0/
    - user: root
    - group: root
    - recurse:
      - user
      - group


hadoop28_de:
  cmd.script:
    - source: salt://utils/de.sh
    - args: "http://www.us.apache.org/dist/hadoop/common/hadoop-2.8.3/hadoop-2.8.3.tar.gz /opt/"
    - creates: /opt/hadoop-2.8.3/
  file.directory:
    - name: /opt/hadoop-2.8.3/
    - user: root
    - group: root
    - recurse:
      - user
      - group

hadoop27_de:
  cmd.script:
    - source: salt://utils/de.sh
    - args: "http://www.us.apache.org/dist/hadoop/common/hadoop-2.7.5/hadoop-2.7.5.tar.gz /opt/"
    - creates: /opt/hadoop-2.7.5/
  file.directory:
    - name: /opt/hadoop-2.7.5/
    - user: root
    - group: root
    - recurse:
      - user
      - group

hadoop_path:
  file.append:
    - name: /etc/profile.d/path_additions.sh
    - text:
      - export HADOOP_VERSION=__HADOOP_VERSION__
      - export PATH=$PATH:/opt/$HADOOP_VERSION/bin

hadoop_env:
  file.append:
    - name: /etc/profile.d/hadoop_env.sh
    - text:
      - export HADOOP_PREFIX=/opt/
      - export HADOOP_VERSION=__HADOOP_VERSION__
      - export HADOOP_CONF_DIR=/opt/$HADOOP_VERSION/etc/hadoop