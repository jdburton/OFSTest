/etc/selinux/config:
  file.replace:
    - pattern: 'SELINUX=enforcing'
    - repl: 'SELINUX=permissive'

include:
  - fedora_states.upgrade_pkgs
  - fedora_states.pkgs
  - fedora_states.environment
