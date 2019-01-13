#!/usr/bin/python
# -*- coding: latin-1 -*-

import sys
import subprocess

subprocess.call("sudo apt-get update", shell=True)
subprocess.call("sudo apt-get -y install mariadb-server", shell=True)
subprocess.call("sudo sed -i -e 's/bind-address.*/bind-address=0.0.0.0/' -e 's/utf8mb4/utf8/' /etc/mysql/mariadb.conf.d/50-server.cnf", shell=True

subprocess.call("sudo mysqladmin -u root password xxxx", shell=True)
subprocess.call("sudo mysql -u root --password='xxxx' -e \"echo CREATE USER 'quiz' IDENTIFIED BY 'xxxx';\"", shell=True)
subprocess.call("sudo mysql -u root --password='xxxx' -e \"echo CREATE DATABASE quiz;\"", shell=True)
subprocess.call("sudo mysql -u root --password='xxxx' -e \"echo GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'localhost' IDENTIFIED by 'xxxx';\"", shell=True)
subprocess.call("sudo mysql -u root --password='xxxx' -e \"echo GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'%' IDENTIFIED by 'xxxx';\"", shell=True)
subprocess.call("sudo mysql -u root --password='xxxx' -e \"echo FLUSH PRIVILEGES;\"", shell=True)

subprocess.call("sudo systemctl restart mysql", shell=True)
