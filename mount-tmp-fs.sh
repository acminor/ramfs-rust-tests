#!/bin/bash

mdir=/tmp/mount

# create the mounting point if it doesn't exit
if [ ! -d ${mdir} ]; then
    mkdir ${mdir}
fi

# mount it!
mount -t ramfs -o size=1m ramfs ${mdir}

