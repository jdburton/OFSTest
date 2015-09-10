salt-master:
  service.running:
    - enable: True

salt-minion:
  service.running:
    - enable: True

sleep 10:
  cmd.run

salt-key -y -a saltMasterMinion:
  cmd.run

salt '*' test.ping:
  cmd.run
