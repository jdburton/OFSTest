db4_de:
  cmd.script:
    - source: salt://utils/de.sh
    - args: "https://s3.amazonaws.com/cloudycluster/ami_src_depends/db-4.8.30.tar.gz /usr/src/"
    - creates: /usr/src/db-4.8.30/
  file.directory:
    - name: /usr/src/db-4.8.30/
    - user: root
    - group: root
    - recurse:
      - user
      - group


torque_de:
  cmd.script:
    - source: salt://utils/de.sh
    - args: "https://s3.amazonaws.com/cloudycluster/ami_src_depends/torque-5.0.1-1_4fa836f5.tar.gz /usr/src/"
    - creates: /usr/src/torque-5.0.1-1_4fa836f5/
  file.directory:
    - name: /usr/src/torque-5.0.1-1_4fa836f5/
    - user: root
    - group: root
    - recurse:
      - user
      - group

maui_de:
  cmd.script:
    - source: salt://utils/de.sh
    - args: "https://s3.amazonaws.com/cloudycluster/ami_src_depends/maui-3.3.1.tar.gz /usr/src/"
    - creates: /usr/src/maui-3.3.1/
  file.directory:
    - name: /usr/src/maui-3.3.1/
    - user: root
    - group: root
    - recurse:
      - user
      - group

maven_de:
  cmd.script:
    - source: salt://utils/de.sh
    - args: "http://archive.apache.org/dist/maven/maven-3/3.2.5/binaries/apache-maven-3.2.5-bin.tar.gz /opt"
    - creates: /opt/apache-maven-3.2.5/
  file.directory:
    - name: /opt/apache-maven-3.2.5/
    - user: root
    - group: root
    - recurse:
      - user
      - group

openmpi_de:
  cmd.script:
    - source: salt://utils/de.sh
#    - args: "https://s3.amazonaws.com/cloudycluster/ami_src_depends/openmpi-1.8.4.tar.gz /usr/src/"
#    - args: "http://devorange.clemson.edu/pvfs/openmpi-1.8.8-omnibond.tar.gz /opt/mpi/"
    - args: "http://52.38.65.99/pvfs/openmpi-1.8.8-omnibond.tar.gz /opt/mpi/"
    - creates: /opt/mpi/openmpi-1.8.8/
  file.directory:
    - name: /opt/mpi/openmpi-1.8.8/

hdf5_de:
  cmd.script:
    - source: salt://utils/de.sh
    - args: "https://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.8.17.tar.gz /usr/src/"
    - creates: /opt/hdf5-1.8.17/
  file.directory:
    - name: /opt/hdf5-1.8.17/
    - user: root
    - group: root
    - recurse:
      - user
      - group
