/swapfile:
  cmd.run:
    - name: "/bin/dd if=/dev/zero of=/swapfile bs=1M count=2048 && chmod 600 /swapfile && mkswap /swapfile"
    - creates: /swapfile
  mount.swap:
    - persist: True
    - require:
      - cmd: /swapfile
