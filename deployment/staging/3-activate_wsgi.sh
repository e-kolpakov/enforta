#!/bin/bash
sudo cp ./3.1-doc-approval-site /etc/apache2/sites-available/doc-approval
sudo a2ensite doc-approval
sudo a2dissite default
sudo apache2ctl restart
