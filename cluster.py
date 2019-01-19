#!/usr/bin/python

import time
import sys
import os
import socket

#Instalacion gluster 
os.system("gluster peer probe 20.2.4.22")
os.system("gluster peer probe 20.2.4.23")
os.system("gluster volume create nas replica 3 20.2.4.21:/nas 20.2.4.22:/nas 20.2.4.23:/nas force")
os.system("gluster volume start nas")
