#!/usr/bin/env bash
#
# This script will localize the file manager
# so that all of the paths are localized to
# the current location of the template repo.

sed "s|PWD|$(pwd)|g" template_file_manager.txt > file_manager.txt
