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
  #'G@os:openSUSE or P@os:openSUSE?Leap or G@os:openSUSE Leap':
  'os_family:Suse':
    - match: grain
    - ofstest_opensuse
#  'G@os_family:Suse and not G@os:openSUSE and not P@os:openSUSE?Leap':
  #'G@os_family:Suse':
#    - match: compound
#    - ofstest_suse
  # Ubuntu based systems
  'os:Ubuntu':
    - match: grain
    - ofstest_ubuntu
  'os:Debian':
    - match: grain
    - ofstest_ubuntu
    