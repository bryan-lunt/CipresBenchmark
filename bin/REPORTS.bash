#!/bin/bash

#change this to point to wheverever your cipressubmit is installed. If it's already on your path, then this line is not needed.
export PATH=$PATH:/home/blunt/opt/cypressubmit/src

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT_ABS_PATH=$(readlink -f $0)
# Absolute path to the directory this script is in. /home/user/bin
SCRIPT_ABS_DIR=$(dirname $SCRIPT_ABS_PATH)
BENCHMARK_SYS_DIR=$(dirname $SCRIPT_ABS_DIR)

(cd ${BENCHMARK_SYS_DIR} ; PYTHONDONTWRITEBYTECODE="true" ./bin/collectResults.py; )

