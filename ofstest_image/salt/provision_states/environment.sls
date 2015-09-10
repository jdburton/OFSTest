/etc/profile.d/ec2.sh:
  file.append:
    - text: export EC2_HOME=ec2-api-tools-1.7.3.0

/etc/profile.d/path_additions.sh:
  file.append:
    - text: export PATH=$PATH:/opt/ec2-api-tools-1.7.3.0/bin:/opt/torque/bin:/opt/torque/sbin:/opt/orangefs/bin:/opt/orangefs/sbin:/opt/db4/bin:/opt/openmpi/bin:/opt/maui/bin:/opt/maui/sbin

/etc/profile.d/python_eggs.sh:
  file.append:
    - text: export PYTHON_EGG_CACHE=/tmp/python-eggs

    
/etc/profile.d/maven.sh:
  file.append:
    - text: 
      - export M2_HOME=/opt/maven
      - export M2=/opt/maven/bin
    