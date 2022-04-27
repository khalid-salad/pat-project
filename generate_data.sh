#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

function usage {
	echo "Usage: $(basename $0) [-m MODE]" 2>&1
	echo "Generate Numpy test report."
	echo "    -m MODE        'fast' or 'full' (default fast)"
	echo "    -b             rebuild numpy in /tmp folder"
}

function build {
        git clone git@github.com:numpy/numpy.git $NUMPYDIR --branch v1.21.6; 
        python3.9 -m pip install -r $NUMPYDIR/test_requirements.txt;
        python3.9 $NUMPYDIR/runtests.py --mode $MODE --coverage;
        python3.9 $NUMPYDIR/runtests.py --mode $MODE --gcov;
        python3.9 $NUMPYDIR/runtests.py --mode $MODE --lcov-html;
        for DIR in lcov coverage; do
            if [ -d $DIR ]; then
                rm -rf $DIR
            fi
            cp -r $NUMPYDIR/build/$DIR ./
	done
}

DIR=/tmp
NUMPYDIR=$DIR/numpy
optstring=":m:b"
MODE="fast"
BUILD=false
while getopts $optstring arg; do
    case $arg in
      m) 
	 MODE=$OPTARG
	 ;;
      b)
	 BUILD=true
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

if [ $BUILD == true ]; then
    if [ -d $NUMPYDIR ]; then
    	echo "Found Numpy folder in $DIR. Removing.";
    	rm -rf $NUMPYDIR;
    fi
    build
elif ! [ -d $NUMPYDIR ]; then
    echo "No Numpy folder in $DIR. Building";
    build
fi

TESTCSV="./test.csv"
PRODCSV="./prod.csv"

for FILE in $TESTCSV $PRODCSV; do
	if [ -f $FILE ]; then
		rm $FILE
		touch $FILE
		echo "file,number of assertions" >> $FILE
	fi
done

TESTFILES=$(find "$NUMPYDIR" -type f -wholename "*/tests/*.py")
echo "There are $(echo "$TESTFILES" | wc --lines) test files"

while IFS= read -r file ; do
	echo "$(basename $file), $(cat $file | grep assert | wc --lines)" >> $TESTCSV
done < <(echo "$TESTFILES")

PRODFILES=$(find "$NUMPYDIR" -type f ! -wholename "*/tests/*" -wholename "*.py")
echo "There are $(echo "$PRODFILES" | wc --lines) production (Python) files"

while IFS= read -r file ; do
	echo "$(basename $file), $(cat $file | grep assert | wc --lines)" >> $PRODCSV
done < <(echo "$PRODFILES")
