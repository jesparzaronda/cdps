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
	os.system("mkdir PracticaFinal")
	os.chdir("PracticaFinal")
	print(" ---- DESCARGA DE LA MAQUINA ----")
	os.system("wget http://idefix.dit.upm.es/cdps/pfinal/pfinal.tgz")
	print(" ---- DESCOMPRIMIENDO ARCHIVOS ----")
	os.system("sudo vnx --unpack pfinal.tgz")
	os.chdir("pfinal")
	print(" ---- MAQUINA CREADA ----")

	# Comprueba si es un ordenador del laboratorio o no.
	if (re.match("/(l[0-9]{3})/", socket.gethostname())):
		print(" ---- EJECUTANDO EN EL LABORATORIO ----")
		os.system("./bin/prepare-pfinal-labo")
	else:
		print(" ---- EJECUTANDO DESDE UN PC ----")
		os.system("./bin/prepare-pfinal-vm")

	os.system("sudo vnx -f pfinal.xml -v --destroy")
	os.system("sudo vnx -f pfinal.xml -v --create")
	print(" ---- ESCENARIO DESPLEGADO ----")



	print(" ---- CONFIGURACION DE SERVIDOR BASE DE DATOS ----")
	i = 0
	while(i < 2):
		os.system("sudo lxc-attach --clear-env -n bbdd -- wget https://raw.githubusercontent.com/jesparzaronda/cdps/master/bbdd.py")
		i = i + 1
	os.system("sudo lxc-attach --clear-env -n bbdd -- python /bbdd.py")
	os.system("sudo lxc-attach --clear-env -n bbdd -- rm /bbdd.py*")

	print(" ---- FINAL CONFIGURACION DE SERVIDOR BASE DE DATOS ----")




	print(" ---- CONFIGURACION DE GLUSTERFS DE ALMACENAMIENTO ----")
	n=3 
	while (n > 0):
		i = 0
		while(i < 2):
			os.system("sudo lxc-attach --clear-env -n nas" +str(n)+ " -- wget https://raw.githubusercontent.com/jesparzaronda/cdps/master/cluster.py")
			i = i + 1
		os.system("sudo lxc-attach --clear-env -n nas" +str(n)+ " -- python /cluster.py")
		os.system("sudo lxc-attach --clear-env -n nas" +str(n)+ " -- rm /cluster.py*")
		n=n-1
	#Instalacion gluster 
	os.system("sudo lxc-attach --clear-env -n nas1 -- gluster peer probe nas2")
	time.sleep(3)

	os.system("sudo lxc-attach --clear-env -n nas1 -- gluster peer probe nas3")
	time.sleep(3)

	os.system("sudo lxc-attach --clear-env -n nas1 -- gluster volume create nas replica 3 nas1:/nas nas2:/nas nas3:/nas force")
	time.sleep(3)

	os.system("sudo lxc-attach --clear-env -n nas1 -- gluster volume start nas")
	time.sleep(3)


	os.system("sudo lxc-attach --clear-env -n nas1 -- gluster volume set nas network.ping-timeout 5")
	os.system("sudo lxc-attach --clear-env -n nas2 -- gluster volume set nas network.ping-timeout 5")
	os.system("sudo lxc-attach --clear-env -n nas3 -- gluster volume set nas network.ping-timeout 5")


	print(" ---- FINAL CONFIGURACION DE CLUSTER DE ALMACENAMIENTO ----")



	print(" ---- INICIO CONFIGURACION QUIZ ----")
	n = 3
	while (n > 0):
		i = 0
		while(i < 2):
			os.system("sudo lxc-attach --clear-env -n s" +str(n)+ " -- wget https://raw.githubusercontent.com/jesparzaronda/cdps/master/node.py")
			i = i + 1
		os.system("sudo lxc-attach --clear-env -n s" +str(n)+ " -- python /node.py")

		print(" ---- CLONACION DEL QUIZ ----")
		os.system("sudo lxc-attach --clear-env -n s" +str(n)+ " -- git clone https://github.com/CORE-UPM/quiz_2019.git")

		print(" ---- INICIO INSTALACION NPM ----")
		os.system("sudo lxc-attach --clear-env -n s" +str(n)+ " -- bash -c \"cd QUIZ_2019; mkdir public/uploads; npm install; npm install forever;npm install mysql2\"")
		print(" ---- FIN INSTALACION NPM ----")

		if n==1:
			os.system("sudo lxc-attach --clear-env -n s1 -- bash -c \" cd /QUIZ_2019; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz; npm run-script migrate_cdps ; npm run-script seed_cdps; ./node_modules/forever/bin/forever start ./bin/www \"")
		else:
			os.system("sudo lxc-attach --clear-env -n s" +str(n)+ " -- bash -c \" cd /QUIZ_2019; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz; ./node_modules/forever/bin/forever start ./bin/www \"")

		os.system("sudo lxc-attach --clear-env -n s" +str(n)+ " -- sudo iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 3000")
		
		os.system("sudo lxc-attach --clear-env -n s" +str(n)+ " -- rm /node.py*")
		
		#Configuracion del sistema de ficheros NAS en servidores
		os.system("sudo lxc-attach --clear-env -n s" +str(n)+ " -- mkdir /QUIZ_2019/public/uploads")
		os.system("sudo lxc-attach --clear-env -n s" +str(n)+ " -- mount -t glusterfs 20.2.4.2" +str(n)+ ":/nas /QUIZ_2019/public/uploads")
		print(" ---- directorio de imágenes creado en s" +str(n)+ " ----")

		n = n -1
	print(" ---- FIN CONFIGURACION DEL QUIZ ----")

	#Configuracion de lb 
	os.system(" xterm -hold -e 'sudo lxc-attach --clear-env -n lb -- xr --verbose --server tcp:0:80 -dr -S --backend 20.2.3.11:80 --backend 20.2.3.12:80 --backend 20.2.3.13:80 --web-interface 0:8001' &")

	print(" ---- CONFIGURACION DE FIREWALL ----")
	# Configuracion de FW desde la carpeta PracticaFinal 
	
	i = 0
	while(i < 2):
		os.system("sudo lxc-attach --clear-env -n fw -- wget https://raw.githubusercontent.com/jesparzaronda/cdps/master/firewall.fw")
		i = i + 1
	os.system("sudo lxc-attach --clear-env -n fw -- sh /firewall.fw")
	os.system("sudo lxc-attach --clear-env -n fw -- rm /firewall.fw.*")
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