db4_install:
  cmd.script:
    - source: salt://src_installs/db4.sh
    - creates: /opt/db4/

torque_install:
  cmd.script:
    - source: salt://src_installs/torque.sh
    - creates: /opt/torque/

maui_install:
  cmd.script:
    - source: salt://src_installs/maui.sh
    - creates: /opt/maui/

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
    - creates: /opt/openmpi/

hdf5_install:
  cmd.script:
    - source: salt://src_installs/hdf5.sh
    - creates: /opt/hdf5/

orangefs_test_install:
  cmd.script:
    - source: salt://src_installs/orangefs_tests.sh
    - creates: /opt/orangefs/test