#!/usr/bin/python

import time
import sys
import os
import socket


print(" ---- CLONACION DEL QUIZ ----")
os.system("cd root")
os.system("git clone https://github.com/CORE-UPM/quiz_2019.git")

print(" ---- INICIO INSTALACION NPM ----")
os.system("cd quiz_2019")
os.system("mkdir public/uploads")
os.system("npm install")
os.system("npm install forever")
os.system("npm install mysql2")
