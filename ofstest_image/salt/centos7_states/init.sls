/etc/selinux/config:
  file.replace:
    - pattern: 'SELINUX=enforcing'
    - repl: 'SELINUX=permissive'

include:
  - centos7_states.upgrade_pkgs
  - centos7_states.pkgs
  - centos7_states.environment
