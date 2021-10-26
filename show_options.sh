#!/bin/bash
# Testing script for ramfs_show_options(). This is invoked when running the
# 'mount' command without any additional arguments (a summary of mounts
# are printed out).
#
#   Connor Shugg

verbose=0
mdir1=/tmp/ramfs_show_options_mount1
mdir2=/tmp/ramfs_show_options_mount2

# Verbose echo.
function __vecho()
{
    if [ ${verbose} -ne 0 ]; then
        echo $@
    fi
}

# Function to create a mount directory and mount it
function __mount_and_test()
{
    # grab arguments
    mdir=$1
    mode=$2

    # set up the mode string, if given
    mode_str=""
    if [ ! -z ${mode} ]; then
        mode_str=",mode=${mode}"
    fi
    
    # create the directory and mount
    mkdir ${mdir}
    mount -t ramfs -o size=1m${mode_str} ramfs ${mdir}
    
    # run 'mount' and search for the output we're interested in
    out="$(mount | grep ${mdir})"
    if [ -z "${out}" ]; then
        __vecho "Failure: mount not created."
        return -1
    fi
    __vecho "Success: found mount: '${out}'"
    
    # make sure the mode is displayed, if we were given one
    if [ ! -z ${mode} ]; then
        if [[ "${out}" == *",mode=${mode}"* ]]; then
            __vecho "Success: found mode: '${out}'"
            return 0
        fi
        
        __vecho "Failure: couldn't find mode '${mode}' in output: '${out}'"
        return -1
    fi
    return 0
}

# Function that unmounts and deletes a mounted ramfs directory.
function __unmount_and_delete()
{
    mdir=$1
    umount ${mdir}
    rm -rf ${mdir}
}

# look for '-v' to enable verbose prints
if [ $# -ge 1 ] && [[ "$1" == "-v" ]]; then
    verbose=1
fi

# TEST 1: default mode
__mount_and_test ${mdir1}
retval=$?
if [ ${retval} -ne 0 ]; then
    exit ${retval}
fi
__unmount_and_delete ${mdir1}

# TEST 2: different mode
__mount_and_test ${mdir2} "644"
retval=$?
if [ ${retval} -ne 0 ]; then
    exit ${retval}
fi
__unmount_and_delete ${mdir2}

