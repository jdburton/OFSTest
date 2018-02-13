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

hadoop_path:
  file.append:
    - name: /etc/profile.d/path_additions.sh
    - text: export PATH=$PATH:/opt/hadoop-2.9.0/bin

hadoop_env:
  file.append:
    - name: /etc/profile.d/hadoop_env.sh
    - text:
      - export HADOOP_PREFIX=/opt/hadoop-2.9.0
      - export HADOOP_CONF_DIR=/opt/hadoop-2.9.0/etc/hadoop

