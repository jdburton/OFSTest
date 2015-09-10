/etc/sysconfig/network-scripts/ifcfg-eth1.bak:
  file.managed:
    - source: salt://config/ifcfg-eth1
    - user: root
    - group: root
    - mode: 644

/etc/sysconfig/network-scripts/routescript-eth1:
  file.managed:
    - source: salt://config/routescript-eth1
    - user: root
    - group: root
    - mode: 644
