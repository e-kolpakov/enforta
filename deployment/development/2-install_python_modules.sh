#!/bin/bash
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv DocApproval
workon DocApproval
pip install -r requirements.txt
