/etc/selinux/config:
  file.replace:
    - pattern: 'SELINUX=enforcing'
    - repl: 'SELINUX=permissive'

include:
  - centos6_states.upgrade_pkgs
  - centos6_states.local_pkgs
  - centos6_states.pkgs
  - centos6_states.environment


