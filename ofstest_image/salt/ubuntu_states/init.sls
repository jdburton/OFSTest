include:
  - ubuntu_states.upgrade_pkgs
  # Install Oracle Java before apt-get brings in OpenJDK
  - ubuntu_states.install_oracle_java
  - ubuntu_states.pkgs
  - ubuntu_states.environment
