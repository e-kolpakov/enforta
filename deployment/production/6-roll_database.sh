#!/bin/bash
cd ../../
python ./manage.py syncdb
python ./manage.py migrate --all