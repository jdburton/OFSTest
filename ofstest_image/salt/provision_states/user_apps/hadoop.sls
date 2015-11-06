hadoop_de:
  cmd.script:
    - source: salt://utils/de.sh
    - args: "https://s3.amazonaws.com/cloudycluster/ami_src_depends/user_apps/hadoop-2.6.0.tar.gz /opt/"
    - creates: /opt/hadoop-2.6.0/
  file.directory:
    - name: /opt/hadoop-2.6.0/
    - user: root
    - group: root
    - recurse:
      - user
      - group

hadoop_path:
  file.append:
    - name: /etc/profile.d/path_additions.sh
    - text: export PATH=$PATH:/opt/hadoop-2.6.0/bin

hadoop_env:
  file.append:
    - name: /etc/profile.d/hadoop_env.sh
    - text:
      - export HADOOP_PREFIX=/opt/hadoop-2.6.0
      - export HADOOP_CONF_DIR=/opt/hadoop-2.6.0/etc/hadoop

