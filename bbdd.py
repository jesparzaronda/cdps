#!/usr/bin/python
# -*- coding: latin-1 -*-

import sys
import os

os.system("sudo apt-get update")
os.system("sudo apt-get -y install mariadb-server")
os.system("sudo sed -i -e 's/bind-address.*/bind-address=0.0.0.0/' -e 's/utf8mb4/utf8/' /etc/mysql/mariadb.conf.d/50-server.cnf")

os.system("sudo mysqladmin -u root password xxxx")
os.system("sudo mysql -u root --password='xxxx' -e \"CREATE USER 'quiz' IDENTIFIED BY 'xxxx';\"")
os.system("sudo mysql -u root --password='xxxx' -e \"CREATE DATABASE quiz;\"")
os.system("sudo mysql -u root --password='xxxx' -e \"GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'localhost' IDENTIFIED by 'xxxx';\"")
os.system("sudo mysql -u root --password='xxxx' -e \"GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'%' IDENTIFIED by 'xxxx';\"")
os.system("sudo mysql -u root --password='xxxx' -e \"FLUSH PRIVILEGES;\"")

os.system("sudo systemctl restart mysql")
