#!/bin/bash
cwd=${PWD}
printf '%s %s\n' "${PWD}" "$1"
cd ./packs/$1
name=$1-$(jq -r .version ./manifest)
zip -r -1 $name.l5rcmpack ./* -x *.git*
mv $name.l5rcmpack $cwd
cd $cwd
echo "::set-output name=asset_path::$name.l5rcmpack"


