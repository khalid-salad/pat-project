#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

function usage {
	echo "Usage: $(basename $0) [-m MODE]" 2>&1
	echo "Generate Numpy test report."
	echo "    -m MODE        'fast' or 'full'"
}

DIR=tmp
NUMPYDIR=$DIR/numpy
optstring=":m:"
MODE="fast"
while getopts $optstring arg; do
    case $arg in
      m) 
	 MODE=$OPTARG
	 ;;
      ?)
	 echo "Invalid option: -$OPTARG."
	 usage
	 ;;
    esac
done

if [ $MODE != "fast" ] && [ $MODE != "full" ]; then
       echo "Invalid mode -m $MODE. Defaulting to fast."	
       MODE="fast";
fi

if [ -d $NUMPYDIR ]; then
	echo "Found numpy folder in $DIR. Removing.";
	rm -rf $NUMPYDIR;
fi
git clone git@github.com:numpy/numpy.git $NUMPYDIR --recursive --branch v1.21.6 
python3.9 -m pip install -r $NUMPYDIR/test_requirements.txt
python3.9 $NUMPYDIR/runtests.py --mode $MODE --coverage
python3.9 $NUMPYDIR/runtests.py --mode $MODE --gcov
python3.9 $NUMPYDIR/runtests.py --mode $MODE --lcov-html
