#!/bin/bash
set -x

KERNEL_VER=`uname -r`
KERNEL_VER_SHORT=`uname -r | sed s/-[\d].*//`

#configure linux source
cp /boot/config-${KERNEL_VER} /usr/src/linux-${KERNEL_VER_SHORT}/.config
cd /usr/src/linux-${KERNEL_VER_SHORT}; make oldconfig && make modules_prepare && make prepare
ln -s /lib/modules/${KERNEL_VER}/build/Module.symvers /lib/modules/${KERNEL_VER}/source

if [ ! -f /lib/modules/${KERNEL_VER}/build/include/linux/version.h ] 
then
   ln -s include/generated/uapi/version.h /lib/modules/${KERNEL_VER}/build/include/linux/version.h
fi

# Miscellaneous configuration

/sbin/modprobe -v fuse
chmod a+x /bin/fusermount
chmod a+r /etc/fuse.conf
                
chmod -R a+w /opt
service cups stop
service sendmail stop
service rpcbind start
service nfs restart
/sbin/rpcbind
service slapd start
chkconfig slapd on
mkdir -p /home/bin
mkdir -p /home/nobody
chown nobody:nobody /home/nobody
chown bin:bin /home/bin
