/var/lib/cloud/instance/boot-finished:
  file.absent


include:
  - provision_states.environment
  - provision_states.download_and_extract
  - provision_states.src_installs
  - provision_states.user_apps
