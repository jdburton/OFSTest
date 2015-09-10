# Set up salt prior to launching minion: file roots, pillar roots, minion config, etc.
# http://docs.saltstack.com/en/latest/topics/tutorials/preseed_key.html

salt-minion:
  service.running:
    - enable: True
