from pymongo import MongoClient
from p2pnetwork.Node import Node
import time


class CentralPeer (Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0):

        client = MongoClient('localhost', 27017)

        self.database = client['quickshop']

        users = self.database['user']

        user = self.database.users.find({"ip": host})

        self.node_count = 0

        _id = ""

        if len(list(user.clone())) != 0:
            print("\nBienvenido!")
            for i in user:
                _id = i["node_id"]

            id = _id
            super(CentralPeer, self).__init__(
                host, port, id, callback, max_connections)
        else:
            super(CentralPeer, self).__init__(
                host, port, id, callback, max_connections)

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)

    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    def insert_product(self, post):
        try:

            if len(self.nodes_inbound) > 0:
                node = self.nodes_inbound[self.node_count]
                self.send_to_node(node, {'message': "1001",
                                         'obj': post})
                self.node_count = self.node_count + 1 % len(self.nodes_inbound)
            else:
                self.database.publicaciones.insert_one(post)

        except Exception as e:
            raise e

    def insert_user(self, user: dict):

        try:

            if len(self.nodes_inbound) > 0:

                node = self.nodes_inbound[self.node_count]

                self.send_to_node(node, {'message': "1002",
                                         'obj': user})
                self.node_count = self.node_count + 1 % len(self.nodes_inbound)

            else:
                self.database.usuarios.insert_one(user)

        except Exception as e:
            raise e

    def get_user_by_id(self, id: dict) -> dict:
        try:
            response = []
            for i in self.nodes_inbound:

                self.send_to_node(i, {"message": "2001",
                                      "obj": id})

                time.sleep(0.5)
                response += i.current_message['result']

            for i in self.database.usuarios.find({'id_usuario': id['id_usuario']}):
                aux = {'id_usuario': i['id_usuario'],
                       'nombre_usuario': i['nombre_usuario'],
                       'contraseña_usuario': i['contraseña_usuario'],
                       'telefono_usuario': i['telefono_usuario'],
                       'correo_usuario': i['correo_usuario'],
                       'zona_entrega_usuario': i['zona_entrega_usuario']
                       }
                response += [aux]

            return {'response': response}

        except Exception as e:
            raise e

    def get_user_by_name(self, name: dict) -> dict:
        try:
            response = []
            for i in self.nodes_inbound:

                self.send_to_node(i, {"message": "2002",
                                      "obj": name})

                time.sleep(0.5)
                response += i.current_message['result']

            for i in self.database.usuarios.find({'nombre_usuario': {"$regex": name['nombre']}}):
                aux = {'id_usuario': i['id_usuario'],
                       'nombre_usuario': i['nombre_usuario'],
                       'contraseña_usuario': i['contraseña_usuario'],
                       'telefono_usuario': i['telefono_usuario'],
                       'correo_usuario': i['correo_usuario'],
                       'zona_entrega_usuario': i['zona_entrega_usuario']
                       }
                response += [aux]

            return {'response': response}

        except Exception as e:
            raise e

    def get_product_by_id(self, id: dict) -> dict:
        try:
            response = []
            for i in self.nodes_inbound:

                self.send_to_node(i, {"message": "2003",
                                      "obj": id})

                time.sleep(0.5)
                response += i.current_message['result']

            for i in self.database.publicaciones.find({'id_publicacion': id['id_publicacion']}):
                aux = {'id_publicacion': i['id_publicacion'],
                       'id_usuario': i['id_usuario'],
                       'nombre': i['nombre'],
                       'descripcion': i['descripcion'],
                       'precio': i['precio'],
                       'categorias': i['categorias']
                       }
                response += [aux]

            return {'response': response}

        except Exception as e:
            raise e

    def get_product_by_name(self, name: dict) -> dict:
        try:
            response = []
            for i in self.nodes_inbound:

                self.send_to_node(i, {"message": "2004",
                                      "obj": name})

                time.sleep(0.5)
                response += i.current_message['result']

            for i in self.database.publicaciones.find({'nombre': {'$regex': name['nombre']}}):
                aux = {'id_publicacion': i['id_publicacion'],
                       'id_usuario': i['id_usuario'],
                       'nombre': i['nombre'],
                       'descripcion': i['descripcion'],
                       'precio': i['precio'],
                       'categorias': i['categorias']
                       }
                response += [aux]
            return {'response': response}

        except Exception as e:
            raise e

    def get_product_by_category(self, category: dict) -> dict:
        try:
            response = []
            for i in self.nodes_inbound:

                self.send_to_node(i, {"message": "2005",
                                      "obj": category})

                time.sleep(0.5)
                response += i.current_message['result']

            for i in self.database.publicaciones.find({'categorias': category['categorias']}):
                aux = {'id_publicacion': i['id_publicacion'],
                       'id_usuario': i['id_usuario'],
                       'nombre': i['nombre'],
                       'descripcion': i['descripcion'],
                       'precio': i['precio'],
                       'categorias': i['categorias']
                       }
                response += [aux]

            return {'response': response}

        except Exception as e:
            raise e

    def get_product_by_user_id(self, id: dict) -> dict:
        try:
            response = []
            for i in self.nodes_inbound:

                self.send_to_node(i, {"message": "2006",
                                      "obj": id})

                time.sleep(0.5)
                response += i.current_message['result']

            for i in self.database.publicaciones.find({'id_usuario': id['id_usuario']}):
                aux = {'id_publicacion': i['id_publicacion'],
                       'id_usuario': i['id_usuario'],
                       'nombre': i['nombre'],
                       'descripcion': i['descripcion'],
                       'precio': i['precio'],
                       'categorias': i['categorias']
                       }
                response += [aux]
            return {'response': response}

        except Exception as e:
            raise e
    """ Uso de las modificaciones:
            La aplicación cliente envía un json con el sig. formato:
                {id_usuario/producto: id,
                 campos a modificar:{campos...}
                 }
            
    
    """

    def modify_product(self, obj: dict) -> dict:
        try:

            for i in self.nodes_inbound:
                self.send_to_node(i, {'message': '3001',
                                      'obj': obj})
            self.database.publicaciones.update_one(
                {"id_publicacion": obj['id_publicacion']}, {'$set': obj['campos']})

        except Exception as e:
            raise e

    def modify_user(self, obj: dict) -> dict:
        try:
            for i in self.nodes_inbound:
                self.send_to_node(i, {'message': '3002',
                                      'obj': obj})
            self.database.usuarios.update_one(
                {"id_usuario": obj['id_usuario']}, {'$set': obj['campos']})
        except Exception as e:
            raise e

    def delete_product(self, id: dict):
        try:
            for i in self.nodes_inbound:

                self.send_to_node(i, {"message": "4001",
                                      "obj": id})

            self.database.publicaciones.delete_one(
                {'id_publicacion': id['id_publicacion']})

        except Exception as e:
            raise e

    def delete_user(self, id: dict):
        try:
            for i in self.nodes_inbound:

                self.send_to_node(i, {"message": "4002",
                                      "obj": id})

            self.database.usuarios.delete_one({'id_usuario': id['id_usuario']})

        except Exception as e:
            raise e

    def node_message(self, connected_node, data):
        print("node_message from " + connected_node.id + ": " + str(data))

    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)

    def node_request_to_stop(self):
        print("node is requested to stop!")
