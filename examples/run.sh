#! /bin/bash

# this script is not intended to be run directly
# instead create a link corresponding to one *.py file
# and that *.py file will be executed with the proper pythonpath
PYTHONPATH="$PYTHONPATH:$(dirname $0)/.." python $0.py "$@"
