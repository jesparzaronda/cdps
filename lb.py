#!/usr/bin/python

import sys
import os
import socket



os.system("sudo apt-get update")
os.system("sudo apt-get install haproxy")


fichero = open("/etc/haproxy/haproxy.cfg", "a")
fichero.write("frontend lb \n bind *:80 \n mode http \n default_backend webservers \n")
fichero.write("backend webservers\n mode http \n balance roundrobin \n server s1 20.2.3.11:80 check \n server s2 20.2.3.12:80 check \n server s3 20.2.3.13:80 check \n")
fichero.close()

os.system("sudo service haproxy restart")


	
	    
	    
	    
	    
	    

	  
