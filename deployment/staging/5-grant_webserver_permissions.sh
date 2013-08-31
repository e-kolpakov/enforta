#!/bin/bash
LOG_PATH=/home/john/enforta/log
UPLOAD_PATH=/var/uploads/doc-approval
sudo mkdir -p $LOG_PATH && sudo chown -R john:www-data $LOG_PATH && sudo chmod g+ws -R $LOG_PATH
sudo mkdir -p $UPLOAD_PATH && sudo chown john:www-data $UPLOAD_PATH && sudo chmod 775 $UPLOAD_PATH
