base:
  # Fedora based systems
  'os:Fedora':
    - match: grain
    - ofstest_fedora
  # RHEL6 based systems (Redhat systems that are NOT Fedora)
  #'P@os:(RedHat|CentOS|Scientific.*) and G@osmajorrelease:6':
  'G@os_family:Redhat and not G@os:Fedora and G@osmajorrelease:6':
    - match: compound
    - ofstest_centos6
  # RHEL7 based systems (Redhat systems that are NOT Fedora)
  #'P@os:(RedHat|CentOS|Scientific.*) and G@osmajorrelease:7':
  'G@os_family:Redhat and not G@os:Fedora and G@osmajorrelease:7':
    - match: compound
    - ofstest_centos7
  # SuSE based systems (base image built in SuSE Studio)
  'os_family:Suse':
    - match: grain
    - ofstest_suse
  # Ubuntu based systems
  'os:Ubuntu':
    - match: grain
    - ofstest_ubuntu