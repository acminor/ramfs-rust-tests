#!/usr/bin/env bash

# test both fs and syscalls with mount directory to make
# sure we test the widest possible collection of filesystem calls
#/opt/ltp/runltp -f fs,syscalls -d /tmp/mount > /tmp/ltp-fs-results 2>&1

# actually syscall tests take too long, just do fs for now
/opt/ltp/runltp -f fs -d /tmp/mount > /tmp/ltp-fs-results 2>&1

exit "$(grep /tmp/ltp-fs-results 'INFO: ltp-pan reported all tests PASS' > /dev/null 2>&1)"
