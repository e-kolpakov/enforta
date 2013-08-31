#!/bin/bash
VIRTUALENV_NAME=DocApproval
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv $VIRTUALENV_NAME --no-site-packages
workon $VIRTUALENV_NAME && pip install -r requirements.txt
