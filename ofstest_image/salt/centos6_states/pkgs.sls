orangefs_depends:
  pkg.installed:
    - skip_suggestions: True
    - pkgs:
      - gcc 
      - gcc-c++ 
      - gcc-gfortran 
      - openssl 
      - fuse 
      - flex 
      - bison 
      - openssl-devel 
      - kernel-devel 
      - kernel-headers
      - perl 
      - make
      - zip 
      - fuse 
      - fuse-devel 
      - fuse-libs 
      - wget 
      - patch 
      - bzip2 
      - libuuid 
      - libuuid-devel 
      - uuid 
      - uuid-devel 
      - openldap 
      - openldap-devel 
      - openldap-clients 
      - gdb 
      - libtool 
      - libtool-ltdl 
      - xfsprogs-devel 
      - attr 
      - libattr-devel 
      - libacl-devel 
      - bc 
      - libaio 
      - libaio-devel
      - kernel-devel
      - dkms
      - python-pip
      - libxml2-devel
      - openldap-devel
      - apr-devel
      - httpd-devel
      - pam-devel
      - perl-Test-Harness
      - automake: /tmp/automake-1.13.4-6_Oso.noarch.rpm
      - autoconf: /tmp/autoconf-2.69-12.2.noarch.rpm

orangefs_hadoop_depends:
  pkg.installed:
    - skip_suggestions: True
    - pkgs:
      - java-1.7.0-openjdk
      - java-1.7.0-openjdk-devel
      

dev_depends:
  pkg.installed:
    - skip_suggestions: True
    - pkgs:
      - git
      - subversion
      - vim-enhanced
      - htop
      - mod_ssl


other_depends:
  pkg.installed:
    - skip_suggestions: True
    - pkgs:
      - unzip
      - boost-devel
      - python-pip
      - time
      - environment-modules
