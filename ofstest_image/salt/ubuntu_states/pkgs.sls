orangefs_depends:
  pkg.installed:
    - skip_suggestions: True
    - pkgs:
      - openssl 
      - gcc 
      - g++ 
      - gfortran 
      - flex 
      - bison 
      - libssl-dev 
      - linux-source 
      - perl 
      - make 
      - linux-headers
      - zip 
      - subversion 
      - automake 
      - autoconf
      - pkg-config 
      - rpm 
      - patch 
      - libuu0 
      - libuu-dev 
      - libuuid1 
      - uuid 
      - uuid-dev 
      - uuid-runtime 
      - gdb 
#      - maven 
      - git 
      - libtool 
      - libacl1-dev 
      - xfslibs-dev 
      - xfsprogs 
      - libdm0-dev 
      - fuse 
      - libfuse2 
      - libfuse-dev
      - slapd 
      - ldap-utils 
      - libldap-2.4-2
      - libldap2-dev 
      - libldap-ocaml-dev
      - bzip2
      - libtool 
      - libltdl7
      - libltdl-dev
      - xfsprogs
      - xfslibs-dev 
      - attr 
      - libattr1
      - libattr1-dev
      - libacl1 
      - libacl1-dev 
      - bc 
      - libaio1 
      - libaio-dev
      - libxml2-dev
      - autotools-dev
      

#orangefs_hadoop_depends:
#  pkg.installed:
#    - skip_suggestions: True
#    - pkgs:
#      - openjdk-7-jdk 
#      - openjdk-7-jre 
#      - openjdk-7-jre-lib
      

dev_depends:
  pkg.installed:
    - skip_suggestions: True
    - pkgs:
      - git
      - subversion
#      - vim-enhanced
#      - htop
#      - mod_ssl
      - libapache2-mod-gnutls


other_depends:
  pkg.installed:
    - skip_suggestions: True
    - pkgs:
      - unzip
      - libboost-dev
      - python-pip
      - time
#      - nmap-ncat
      - environment-modules
  

