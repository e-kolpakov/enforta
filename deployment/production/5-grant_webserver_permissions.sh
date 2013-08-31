#!/bin/bash
LOG_PATH=/home/enfortit/docapproval/log
UPLOAD_PATH=/var/uploads/doc-approval
sudo mkdir -p $LOG_PATH && sudo chown -R enfortit:www-data $LOG_PATH && sudo chmod g+ws -R $LOG_PATH
sudo mkdir -p $UPLOAD_PATH && sudo chown www-data $UPLOAD_PATH && sudo chmod 775 $UPLOAD_PATH
