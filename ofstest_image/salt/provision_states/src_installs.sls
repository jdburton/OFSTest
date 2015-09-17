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

#openmpi_install:
#  cmd.script:
#    - source: salt://src_installs/openmpi.sh
#    - creates: /opt/openmpi/
