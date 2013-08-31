#!/bin/bash
LOG_PATH=/home/john/enforta/log
UPLOAD_PATH=/var/uploads/doc-approval
sudo mkdir $LOG_PATH && sudo chown -R john:www-data $LOG_PATH && sudo chmod g+ws -R $LOG_PATH
sudo mkdir -p $UPLOAD_PATH && sudo chown www-data:www-data $UPLOAD_PATH && sudo chmod 775 $UPLOAD_PATH
