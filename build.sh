#!/usr/bin/env bash
DIST_NAME=pyposdisplay
DIST_TYPE=tar.gz
DIST_DIR=dist
BUILD_DIR=build
default_name="Sébastien BEAU"
default_email="sebastien.beau@akretion.com"

read -p "Full name (default $default_name): " fullname
read -p "Email (default $default_email): " email
default_version=$(cat VERSION)-1
read -p "Version: (default $default_version): " version
version=${version:-$default_version}
export DEBFULLNAME=${fullname:-$default_name}
export DEBEMAIL=${email:-$default_email}
debchange -v $version

rm -rf $DIST_DIR $BUILD_DIR
python setup.py sdist
DIST_FILENAME=$(ls $DIST_DIR/*.$DIST_TYPE -1 | tail -n 1 | cut -d'/' -f2)
ORIG_FILENAME=$(echo $DIST_FILENAME | sed "s/$DIST_TYPE/orig.$DIST_TYPE/" | sed "s/\-/_/")

cp $DIST_DIR/$DIST_FILENAME ../python-$ORIG_FILENAME
rm -rf $DIST_DIR $BUILD_DIR

debuild -i -us -uc -b

#cleanup
debclean
