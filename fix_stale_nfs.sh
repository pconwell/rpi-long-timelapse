#!/bin/bash

# crontab:
# * * * * * /root/fix_stale_nfs.sh >/dev/null 2>&1
#
# don't forget to make this script executable with chmod +x

list=$(ls /mnt/unraid)

for i in $list
do
        status=$(ls /mnt/unraid/$i 2>&1)

        if [[ $status =~ .*Stale.* ]]
                then
                umount -f /mnt/unraid/$i
        fi
done

mount -a
