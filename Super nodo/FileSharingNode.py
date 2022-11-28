from pymongo import MongoClient
from p2pnetwork.Node import Node
import time


class FileSharingNode (Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0):

        client = MongoClient('localhost', 27017)

        self.database = client['quickshop']

        users = self.database['user']

        user = self.database.users.find({"ip": host})

        _id = "perro"

        if len(list(user.clone())) != 0:
            print("\nBienvenido!")
            for i in user:
                _id = i["node_id"]

            id = _id
            super(FileSharingNode, self).__init__(
                host, port, id, callback, max_connections)
        else:
            super(FileSharingNode, self).__init__(
                host, port, id, callback, max_connections)

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)

    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    def node_message(self, connected_node, data):
        print("node_message from " + connected_node.id + ": " + str(data))

        if (isinstance(data, dict) and "message" in data.keys()):

            if (data['message'] == "1001"):

                try:
                    obj = data['obj']
                    publicaciones = self.database['publicaciones']
                    result = self.database.publicaciones.insert_one(obj)
                    self.send_to_node(self.super_par, result)

                except Exception as e:
                    self.debug_print(e)
                    raise e
            if (data['message'] == "1002"):
                try:
                    obj = data['obj']
                    usuarios = self.database['usuarios']
                    result = self.database.usuarios.insert_one(obj)
                    self.send_to_node(self.super_par, result)

                except Exception as e:
                    self.debug_print(e)
                    raise e
            if (data['message'] == "2001"):
                try:
                    obj = data['obj']
                    usuarios = self.database['usuarios']

                    resulta = self.database.usuarios.find(
                        {'id_usuario': obj['id_usuario']})

                    result = []
                    for i in resulta:
                        aux = {'id_usuario': i['id_usuario'],
                               'nombre_usuario': i['nombre_usuario'],
                               'contraseña_usuario': i['contraseña_usuario'],
                               'telefono_usuario': i['telefono_usuario'],
                               'correo_usuario': i['correo_usuario'],
                               'zona_entrega_usuario': i['zona_entrega_usuario']
                               }
                        result.append(aux)

                    self.send_to_node(self.super_par, {'result': result})

                except Exception as e:
                    raise e

            if (data['message'] == "2002"):
                try:
                    obj = data['obj']
                    nombre = obj['nombre']
                    usuarios = self.database['usuarios']

                    resulta = self.database.usuarios.find(
                        {'nombre': f"/{nombre}/"})

                    result = []
                    for i in resulta:
                        aux = {'id_usuario': i['id_usuario'],
                               'nombre_usuario': i['nombre_usuario'],
                               'contraseña_usuario': i['contraseña_usuario'],
                               'telefono_usuario': i['telefono_usuario'],
                               'correo_usuario': i['correo_usuario'],
                               'zona_entrega_usuario': i['zona_entrega_usuario']
                               }
                        result.append(aux)

                    self.send_to_node(self.super_par, {'result': result})

                except Exception as e:
                    raise e

            if (data['message'] == "2003"):
                try:
                    obj = data['obj']
                    publicaciones = self.database['publicaciones']

                    resulta = self.database.publicaciones.find(
                        {'id_publicacion': obj['id_publicacion']})

                    result = []
                    for i in resulta:
                        aux = {'id_publicacion': i['id_publicacion'],
                               'id_usuario': i['id_usuario'],
                               'nombre': i['nombre'],
                               'descripcion': i['descripcion'],
                               'precio': i['precio'],
                               'categorias': i['categorias']
                               }
                        result.append(aux)

                    self.send_to_node(self.super_par, {'result': result})

                except Exception as e:
                    raise e

            if (data['message'] == "2004"):
                try:
                    obj = data['obj']
                    nombre = obj['nombre']
                    publicaciones = self.database['publicaciones']

                    resulta = self.database.publicaciones.find(
                        {'nombre': f"/{nombre}/"})

                    result = []
                    for i in resulta:
                        aux = {'id_usuario': i['id_usuario'],
                               'nombre_usuario': i['nombre_usuario'],
                               'contraseña_usuario': i['contraseña_usuario'],
                               'telefono_usuario': i['telefono_usuario'],
                               'correo_usuario': i['correo_usuario'],
                               'zona_entrega_usuario': i['zona_entrega_usuario']
                               }
                        result.append(aux)

                    self.send_to_node(self.super_par, {'result': result})

                except Exception as e:
                    raise e
            if (data['message'] == "2005"):
                try:

                    obj = data['obj']
                    publicaciones = self.database['publicaciones']

                    resulta = self.database.publicaciones.find(
                        {'categorias': obj['categoria']})

                    result = []
                    for i in resulta:
                        aux = {'id_publicacion': i['id_publicacion'],
                               'id_usuario': i['id_usuario'],
                               'nombre': i['nombre'],
                               'descripcion': i['descripcion'],
                               'precio': i['precio'],
                               'categorias': i['categorias']
                               }
                        result.append(aux)

                    self.send_to_node(self.super_par, {'result': result})

                except Exception as e:
                    raise e

            if (data['message'] == "2006"):
                try:
                    obj = data['obj']
                    publicaciones = self.database['publicaciones']

                    resulta = self.database.publicaciones.find(
                        {'id_usuario': obj['id_usuario']})

                    result = []
                    for i in resulta:
                        aux = {'id_publicacion': i['id_publicacion'],
                               'id_usuario': i['id_usuario'],
                               'nombre': i['nombre'],
                               'descripcion': i['descripcion'],
                               'precio': i['precio'],
                               'categorias': i['categorias']
                               }
                        result.append(aux)

                    self.send_to_node(self.super_par, {'result': result})

                except Exception as e:
                    raise e

        if (data['message'] == '3001'):
            try:
                obj = data['obj']

                publicaciones = self.database['publicaciones']
                result = self.database.publicaciones.update(
                    {obj['id_publicacion']}, {'$set': obj['campos']})

                self.send_to_node(self.super_par, {'result', result})

            except Exception as e:
                raise e
        if (data['message'] == '3002'):
            try:
                obj = data['obj']

                usuarios = self.database['usuarios']
                result = self.database.usuarios.update(
                    {obj['id_usuario']}, {'$set': obj['campos']})

                self.send_to_node(self.super_par, {'result', result})

            except Exception as e:
                raise e

        if (data['message'] == '4001'):
            try:
                self.database.publicaciones.delete_one(
                    {'id_publicacion': id['id_publicacion']})
            except Exception as e:
                raise e
        if (data['message'] == '4002'):
            try:
                self.database.usuarios.delete_one(
                    {'id_usuario': id['id_usuario']})
            except Exception as e:
                raise e

    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)

    def node_request_to_stop(self):
        print("node is requested to stop!")
