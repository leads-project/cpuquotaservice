#!/bin/bash
set -o nounset
set -o errexit

BASEDIR=`dirname $0`

activate () {
  set +u
  . ./cpuquota_virtualenv/bin/activate
  set -u
}

virtualenv cpuquota_virtualenv

activate

pip install -r requirements.txt
