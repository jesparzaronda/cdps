#!/usr/bin/python
# -*- coding: latin-1 -*-

os.system("sudo apt-get update")
os.system("sudo apt-get upgrade")
os.system("sudo apt-get install software-properties-common")
os.system("ssudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8")
os.system("sudo add-apt-repository 'deb [arch=amd64,arm64,ppc64el] http://tedeco.fi.upm.es/mirror/mariadb/repo/10.1/ubuntu bionic main'")

os.system("sudo apt-get update")
os.system("sudo apt-get -y install mariadb-server")
os.system("sudo sed -i -e 's/bind-address.*/bind-address=0.0.0.0/' -e 's/utf8mb4/utf8/' /etc/mysql/mariadb.conf.d/50-server.cnf")

os.system("sudo mysqladmin -u root password xxxx")
os.system("sudo mysql -u root --password='xxxx' -e echo \"CREATE USER 'quiz' IDENTIFIED BY 'xxxx';\"")
os.system("sudo mysql -u root --password='xxxx' -e echo \"CREATE DATABASE quiz;\"")
os.system("sudo mysql -u root --password='xxxx' -e echo \"GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'localhost' IDENTIFIED by 'xxxx';\"")
os.system("sudo mysql -u root --password='xxxx' -e echo \"GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'%' IDENTIFIED by 'xxxx';\"")
os.system("sudo mysql -u root --password='xxxx' -e echo \"FLUSH PRIVILEGES;\"")

os.system("sudo systemctl restart mysql")
