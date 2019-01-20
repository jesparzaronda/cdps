#!/usr/bin/python
# -*- coding: latin-1 -*-

import time
import sys
import os
import socket
import re

def despliegue():

	if (os.path.isdir("ProyectoFinal")):
		os.system("sudo rm -rf ProyectoFinal")

	print(" ---- CREANDO CARPETA ----")
	os.system("mkdir ProyectoFinal")
	os.chdir("ProyectoFinal")
	print(" ---- DESCARGA DE LA MAQUINA ----")
	os.system("wget http://idefix.dit.upm.es/cdps/pfinal/pfinal.tgz")
	print(" ---- DESCOMPRIMIENDO ARCHIVOS ----")
	os.system("sudo vnx --unpack pfinal.tgz")
	os.chdir("pfinal")
	print(" ---- MAQUINA CREADA ----")

	print(" ---- EJECUTANDO DESDE UN PC ----")
	os.system("bin/prepare-pfinal-vm")

	os.system("sudo vnx -f pfinal.xml -v --destroy")
	os.system("sudo vnx -f pfinal.xml -v --create")
	print(" ---- ESCENARIO DESPLEGADO ----")



	print(" ---- CONFIGURACION DE SERVIDOR BASE DE DATOS ----")	

	os.system("sudo lxc-attach --clear-env -n bbdd -- wget https://raw.githubusercontent.com/jesparzaronda/cdps/master/bbdd.py")		
	os.system("sudo lxc-attach --clear-env -n bbdd -- python /bbdd.py")

	print(" ---- FINAL CONFIGURACION DE SERVIDOR BASE DE DATOS ----")




	print(" ---- CONFIGURACION DE GLUSTERFS DE ALMACENAMIENTO ----")
	
	os.system("sudo lxc-attach --clear-env -n nas1 -- wget https://raw.githubusercontent.com/jesparzaronda/cdps/master/cluster.py")
	os.system("sudo lxc-attach --clear-env -n nas1 -- python /cluster.py")
	os.system("sudo lxc-attach --clear-env -n nas1 -- gluster volume set nas network.ping-timeout 5")
	os.system("sudo lxc-attach --clear-env -n nas2 -- gluster volume set nas network.ping-timeout 5")
	os.system("sudo lxc-attach --clear-env -n nas3 -- gluster volume set nas network.ping-timeout 5")

	print(" ---- FINAL CONFIGURACION DE CLUSTER DE ALMACENAMIENTO ----")



	print(" ---- INICIO CONFIGURACION QUIZ ----")
	os.system("sudo lxc-attach --clear-env -n s1 -- wget -P/root/ https://raw.githubusercontent.com/jesparzaronda/cdps/master/node.py")
	os.system("sudo lxc-attach --clear-env -n s2 -- wget -P/root/ https://raw.githubusercontent.com/jesparzaronda/cdps/master/node.py")
	os.system("sudo lxc-attach --clear-env -n s3 -- wget -P/root/ https://raw.githubusercontent.com/jesparzaronda/cdps/master/node.py")
	os.system("sudo lxc-attach --clear-env -n s1 -- python /root/node.py")
	os.system("sudo lxc-attach --clear-env -n s2 -- python /root/node.py")
	os.system("sudo lxc-attach --clear-env -n s3 -- python /root/node.py")

	print(" ---- CLONACION DEL QUIZ ----")
	os.system("sudo lxc-attach --clear-env -n s1 -- git clone https://github.com/CORE-UPM/quiz_2019.git /root/quiz_2019/")
	os.system("sudo lxc-attach --clear-env -n s2 -- git clone https://github.com/CORE-UPM/quiz_2019.git /root/quiz_2019/")
	os.system("sudo lxc-attach --clear-env -n s3 -- git clone https://github.com/CORE-UPM/quiz_2019.git /root/quiz_2019/")

	print(" ---- INICIO INSTALACION NPM ----")
	os.system("sudo lxc-attach --clear-env -n s1 -- bash -c \" cd /root/quiz_2019; mkdir public/uploads; npm install; npm install forever;npm install mysql2\"")
	os.system("sudo lxc-attach --clear-env -n s2 -- bash -c \" cd /root/quiz_2019; mkdir public/uploads; npm install; npm install forever;npm install mysql2\"")
	os.system("sudo lxc-attach --clear-env -n s3 -- bash -c \" cd /root/quiz_2019; mkdir public/uploads; npm install; npm install forever;npm install mysql2\"")
	print(" ---- FIN INSTALACION NPM ----")
	os.system("sudo lxc-attach --clear-env -n s1 -- bash -c \" cd /root/quiz_2019; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz; npm run-script migrate_cdps; npm run-script seed_cdps; ./node_modules/forever/bin/forever start ./bin/www \"")
	os.system("sudo lxc-attach --clear-env -n s2 -- bash -c \" cd /root/quiz_2019; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz; ./node_modules/forever/bin/forever start ./bin/www \"")
	os.system("sudo lxc-attach --clear-env -n s3 -- bash -c \" cd /root/quiz_2019; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz; ./node_modules/forever/bin/forever start ./bin/www \"")

	os.system("sudo lxc-attach --clear-env -n s1 -- sudo iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 3000")
	os.system("sudo lxc-attach --clear-env -n s2 -- sudo iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 3000")
	os.system("sudo lxc-attach --clear-env -n s3 -- sudo iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 3000")
		
		
		
	#Configuracion del sistema de ficheros NAS en servidores
	os.system("sudo lxc-attach --clear-env -n s1 -- mount -t glusterfs 20.2.4.21:/nas /root/quiz_2019/public/uploads")
	os.system("sudo lxc-attach --clear-env -n s2 -- mount -t glusterfs 20.2.4.22:/nas /root/quiz_2019/public/uploads")
	os.system("sudo lxc-attach --clear-env -n s3 -- mount -t glusterfs 20.2.4.23:/nas /root/quiz_2019/public/uploads")

		
	print(" ---- FIN CONFIGURACION DEL QUIZ ----")

	print(" ---- CONFIGURACION DEL BALANCEADOR LB ----")

	os.system("sudo lxc-attach --clear-env -n lb -- wget https://raw.githubusercontent.com/jesparzaronda/cdps/master/lb.py")		
	os.system("sudo lxc-attach --clear-env -n lb -- python /lb.py")

	print(" ---- FIN CONFIGURACION DEL BALANCEADOR LB ----")


	print(" ---- CONFIGURACION DE FIREWALL ----")

	os.system("sudo lxc-attach --clear-env -n fw -- wget https://raw.githubusercontent.com/jesparzaronda/cdps/master/fw.fw")		
    os.system("sudo lxc-attach --clear-env -n fw -- sh /fw.fw")
	print(" ---- FIN DE CONFIGURACION DE FIREWALL ----")

	return

def destroy():
	os.chdir("ProyectoFinal/pfinal/")
	os.system("sudo vnx -f pfinal.xml -v --destroy")
	os.chdir("../../")
	os.system("sudo rm -rf ProyectoFinal")
	return

if sys.argv[1] == "create":
	despliegue()
elif sys.argv[1] == "destroy":
	destroy()
