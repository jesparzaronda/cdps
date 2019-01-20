## Centros de Datos y de Provisión de Servicios
Curso 2018-19.

### Objetivo
Creación de un escenario completo de despliegue de una aplicación fiable y escalable que
integre los diversos contenidos impartidos en la asignatura.

### Descripción
El objetivo de esta práctica es la implementación de la arquitectura completa para el
despliegue de una aplicación de juegos sencilla de forma escalable y fiable. Como aplicación
se utilizará proyecto QUIZ utilizado en la asignatura CORE. En la arquitectura de despliegue
del proyecto se utilizarán los elementos típicos de las arquitecturas actuales: firewall,
balanceador de carga, servidores front-end corriendo la aplicación, bases de datos y
servidores de almacenamiento.

### Instalación
Para instalar el programa ejecutamos en un terminal estas sentencias:
##### wget https://raw.githubusercontent.com/jesparzaronda/cdps/master/principal.py
##### sudo python principal.py create

### Desinstalar
Para borrar todo el programas ejecutamos:
##### sudo python principal.py destroy
