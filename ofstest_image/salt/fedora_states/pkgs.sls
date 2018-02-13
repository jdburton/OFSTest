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
      - automake 
      - autoconf 
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
      - libxml2-devel
      - openldap-devel
      - apr-devel
      - httpd-devel
      - pam-devel
      - perl-Math-BigInt

orangefs_hadoop_depends:
  pkg.installed:
    - skip_suggestions: True
    - pkgs:
      - java-1.8.0-openjdk
      - java-1.8.0-openjdk-devel

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
      - time
      - nmap-ncat
      - environment-modules

