db4_install:
  cmd.script:
    - source: salt://src_installs/db4.sh
    - creates: /opt/db4/

maven_install:
  cmd.script:
    - source: salt://src_installs/maven.sh
    - creates: /usr/bin/mvn

orangefs_install:
  cmd.script:
    - source: salt://src_installs/orangefs.sh
    - creates: /opt/orangefs/

openmpi_install:
  cmd.script:
    - source: salt://src_installs/openmpi.sh
    - creates: /opt/mpi/openmpi-1.8.8

hdf5_install:
  cmd.script:
    - source: salt://src_installs/hdf5.sh
    - creates: /opt/hdf5-1.8.17

orangefs_test_install:
  cmd.script:
    - source: salt://src_installs/orangefs_tests.sh
    - creates: /opt/orangefs/test