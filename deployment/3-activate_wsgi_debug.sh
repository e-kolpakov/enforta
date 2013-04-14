#!/bin/bash
sudo cp ./3.1-doc-approval-site-debug /etc/apache2/sites-available/doc-approval
sudo a2ensite doc-approval
sudo service apache2 reload
sudo apache2ctl restart
