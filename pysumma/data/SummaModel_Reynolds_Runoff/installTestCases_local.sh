#!/bin/bash

# install the test cases that can be run with the ./runTestCases.sh
# the script creates the necessary output directories and sets the
# paths in the model input files.

# check whether the settings, output and/or testCases_data directories already
# exist to prevent overwriting directories in which a user may have made changes
if [ -d settings_copy -o -d data_copy ]
    then
        echo 'settings, output and/or testCases_data directories already exist.'
        echo 'Please remove or move the settings, output and testCases_data'
        echo 'directories to prevent overwriting'
        exit 1
fi
#cp -rp ${DIR}_org ${DIR}
# create the paths for the output files
#mkdir -p output

# modify the paths in the model input file
# we create a new directories to preserve copies of the original files in case
# something goes wrong
BASEDIR=`pwd`
for DIR in settings data
    do
        cp -rp ${DIR} ${DIR}_copy
        for file in `grep -l '<BASEDIR>' -R ${DIR}`
            do
                sed "s|<BASEDIR>|${BASEDIR}|" $file > junk
                mv junk $file
            done
		rm -rf settings_copy settings, data_copy
    done
echo "TestCases installed"
