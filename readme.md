# Back-end del TT 2021-B026: Quick Shop

Este repositorio contiene el Back-end del TT titulado Prototipo de una red distribuida de comercio electrónico entre iguales (P2P) con un modelo de negocios de cliente a cliente (C2C)

## Comandos para iniciar la API
1. Prender el Nodo1 en Azure
2. Acceder a la máquina virtual haciendo uso del protocolo SSH
3. Ejecutar los siguientes comandos en el orden especificado dentro de la terminal  
    `sudo systemctl start mongod`  
    `cd quickshop`  
    `source quickshopenv/bin/activate`  
    `gunicorn --bind 0.0.0.0:5000 wsgi:app`

## Tecnologías utilizadas
- [python-p2p-network](https://github.com/macsnoeren/python-p2p-network) (Biblioteca de python para crear la red P2P)
- [PyMongo](https://www.mongodb.com/docs/drivers/pymongo/) (Driver de MongoDB para aplicaciones síncronas de Python)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/) (Framework web escrito en Python)
- [Gunicorn](https://gunicorn.org/) (Servidor HTTP WSGI escrito en Python para UNIX)
- [MongoDB](https://www.mongodb.com/) (Gestor de base de datos no relacional)

## Interfaz de usuario
La interfaz de usuario usada para este proyecto se encuentra [aqui](https://github.com/MaxCazares/TT-Front-end)