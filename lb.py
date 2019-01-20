#!/usr/bin/python

import sys
import os
import socket



os.system("sudo apt-get update")
os.system("sudo apt-get install haproxy")


fichero = open("/etc/haproxy/haproxy.cfg", "w")
fichero.write("frontend haproxynode \n bind *:80 \n mode http \n default_backend backendnodes \n")
fichero.write("backend backendnodes \n balance roundrobin \n option forwardfor \n http-request set-header X-Forwarded-Port %[dst_port] \n http-request add-header X-Forwarded-Proto https if { ssl_fc } \n server s1 20.2.3.11:8080 check \n server s2 20.2.3.12:8080 check \n server s3 20.2.3.13:8080 check\n")
fichero.write("listen stats \n bind :32700 \n stats enable \n stats uri / \n stats hide-version \n stats auth someuser:password \n")
fichero.close()

os.system("sudo service haproxy restart")


	
	    
	    
	    
	    
	    

	  