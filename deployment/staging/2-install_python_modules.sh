#!/bin/bash
#source /usr/local/bin/virtualenvwrapper.sh
#mkvirtualenv DocApproval --no-site-packages
virtualenv DocApproval --no-site-packages
workon DocApproval
pip install -r requirements.txt
