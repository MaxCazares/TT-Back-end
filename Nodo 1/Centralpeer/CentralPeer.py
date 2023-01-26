from pymongo import MongoClient
from p2pnetwork.Node import Node
from p2pnetwork.Node import NodeConnection
import requests
import base64
import numpy as np
import io
import time


class CentralPeer (Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0):

        client = MongoClient('localhost', 27017)

        self.database = client['quickshop']

        users = self.database['user']

        user = self.database.users.find({"ip": host})
        self.ip = requests.get(
            'https://www.wikipedia.org').headers['X-Client-IP']

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

        self.current_post = self.get_publicacion_random(12)

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
            if len(self.all_nodes) > 0:
                node = self.all_nodes[self.node_count]
                self.send_to_node(node, {'message': "1001",
                                         'obj': post})
                self.node_count = (self.node_count + 1) % len(self.all_nodes)

            self.database.publicaciones.insert_one(post)

        except Exception as e:
            raise e

    def insert_user(self, user: dict):

        try:

            if len(self.all_nodes) > 0:

                node = self.all_nodes[self.node_count]

                self.send_to_node(node, {'message': "1002",
                                         'obj': user})
                self.node_count = (self.node_count + 1) % len(self.all_nodes)

            self.database.usuarios.insert_one(user)

        except Exception as e:
            raise e

    def insert_post_comment(self, comment: dict) -> None:

        try:
            if len(self.all_nodes) > 0:
                node = self.all_nodes[self.node_count]
                self.send_to_node(node, {'message': "1003",
                                         'obj': comment})
                self.node_count = (self.node_count + 1) % len(self.all_nodes)

            self.database.comentariospublicacion.insert_one(comment)

        except Exception as e:
            raise e

    def insert_user_comment(self, comment: dict) -> None:

        try:
            if len(self.all_nodes) > 0:
                node = self.all_nodes[self.node_count]
                self.send_to_node(node, {'message': "1004",
                                         'obj': comment})
                self.node_count = (self.node_count + 1) % len(self.all_nodes)

            self.database.comentariosusuario.insert_one(comment)

        except Exception as e:
            raise e

    def create_chat(self, chat: dict) -> dict:

        try:

            if self.node_count < len(self.all_nodes):

                node = self.all_nodes[self.node_count]

                self.send_to_node(node, {'message': "1005",
                                         'obj': chat})

            else:
                self.database.chats.insert_one(chat)

            self.node_count = self.node_count + 1 % (len(self.all_nodes)+1)

        except Exception as e:
            raise e

    def get_user_by_name(self, name: dict) -> dict:
        try:
            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2002",
                                      "obj": name['nombre']})

                time.sleep(0.025)
                if 'result' in i.current_message.keys():
                    response += i.current_message['result']

            for i in self.database.usuarios.find({'nombre_usuario': {"$regex": name['nombre'], "$options": "i"}}):
                aux = {'id_usuario': i['id_usuario'],
                       'nombre_usuario': i['nombre_usuario'],
                       'contraseña_usuario': i['contraseña_usuario'],
                       'telefono_usuario': i['telefono_usuario'],
                       'correo_usuario': i['correo_usuario'],
                       'zona_entrega_usuario': i['zona_entrega_usuario'],
                       'host': self.ip
                       # 'img_usuario':i['img_usuario']
                       }
                response += [aux]

            ar = []
            ids = []
            for i in response:
                if i['id_usuario'] not in ids:
                    ar.append(i)
                    ids.append(i['id_usuario'])
            response = ar

            return {'response': response}

        except Exception as e:
            raise e

    def get_user_by_id(self, id: dict) -> dict:
        try:
            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2001",
                                      "obj": id['id_usuario']})

                time.sleep(0.025)
                if 'result' in i.current_message.keys():
                    response += i.current_message['result']

            for i in self.database.usuarios.find({'id_usuario': id['id_usuario']}):
                aux = {'id_usuario': i['id_usuario'],
                       'nombre_usuario': i['nombre_usuario'],
                       'contraseña_usuario': i['contraseña_usuario'],
                       'telefono_usuario': i['telefono_usuario'],
                       'correo_usuario': i['correo_usuario'],
                       'zona_entrega_usuario': i['zona_entrega_usuario'],
                       'host': self.ip
                       # 'img_usuario':i['img_usuario']
                       }
                response += [aux]

            if len(response) > 1:
                for i in response:
                    if "id_usuario" in i.keys():
                        response = [i]
                        break
            return {'response': response}

        except Exception as e:
            raise e

    def get_user_by_email(self, email: dict) -> dict:

        try:
            response = []

            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2011",
                                      "obj": email["email"]})
                time.sleep(0.025)
                if 'result' in i.current_message.keys():

                    response += i.current_message['result']

            print("Buscando en base de datos...")

            for i in self.database.usuarios.find({'correo_usuario': email["email"]}):
                aux = {'id_usuario': i['id_usuario'],
                       'nombre_usuario': i['nombre_usuario'],
                       'contraseña_usuario': i['contraseña_usuario'],
                       'telefono_usuario': i['telefono_usuario'],
                       'correo_usuario': i['correo_usuario'],
                       'zona_entrega_usuario': i['zona_entrega_usuario'],
                       'host': self.ip
                       # 'img_usuario':i['img_usuario']
                       }

                response += [aux]
            if len(response) > 1:
                for i in response:
                    if "id_usuario" in i.keys():
                        response = [i]
                        break

            return {"response": response}

        except Exception as e:
            raise e
            return {"response": []}

    def get_product_by_id(self, id: dict) -> dict:
        try:
            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2003",
                                      "obj": id['id_publicacion']})

                time.sleep(0.025)
                if 'result' in i.current_message.keys():
                    response += i.current_message['result']

            for i in self.database.publicaciones.find({'id_publicacion': id['id_publicacion']}):
                aux = {'id_publicacion': i['id_publicacion'],
                       'id_usuario': i['id_usuario'],
                       'nombre': i['nombre'],
                       'descripcion': i['descripcion'],
                       'precio': i['precio'],
                       'categoria': i['categoria'],
                       'host': self.ip
                       # 'img_list':i['img_list']
                       }
                response += [aux]

            if len(response) > 1:
                for i in response:
                    if "id_publicacion" in i.keys():
                        response = [i]
                        break
            return {'response': response}

        except Exception as e:
            raise e

    def get_product_by_name(self, name: dict) -> dict:
        try:
            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2004",
                                      "obj": name['nombre']})

                time.sleep(0.025)
                if 'result' in i.current_message.keys():
                    response += i.current_message['result']

            for i in self.database.publicaciones.find({'nombre': {'$regex': name['nombre'], "$options": "i"}}):
                aux = {'id_publicacion': i['id_publicacion'],
                       'id_usuario': i['id_usuario'],
                       'nombre': i['nombre'],
                       'descripcion': i['descripcion'],
                       'precio': i['precio'],
                       'categoria': i['categoria'],
                       'host': self.ip
                       # 'img_list':i['img_list']
                       }
                response += [aux]

            ar = []
            ids = []
            for i in response:
                if i['id_publicacion'] not in ids:
                    ar.append(i)
                    ids.append(i['id_publicacion'])
            response = ar

            return {'response': response}

        except Exception as e:
            raise e

    def get_product_by_category(self, category: dict) -> dict:
        try:
            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2005",
                                      "obj": category["categoria"]})

                time.sleep(0.025)

                if "result" in i.current_message.keys():
                    response += i.current_message['result']

            for i in self.database.publicaciones.find({'categoria': {"$regex": category['categoria'], "$options": "i"}}):
                aux = {'id_publicacion': i['id_publicacion'],
                       'id_usuario': i['id_usuario'],
                       'nombre': i['nombre'],
                       'descripcion': i['descripcion'],
                       'precio': i['precio'],
                       'categoria': i['categoria'],
                       'host': self.ip
                       # 'img_list':i['img_list']
                       }
                response += [aux]

            ar = []
            ids = []
            for i in response:
                if i['id_publicacion'] not in ids:
                    ar.append(i)
                    ids.append(i['id_publicacion'])
            response = ar
            return {'response': response}

        except Exception as e:
            raise e

    def get_product_by_user_id(self, id: dict) -> dict:
        try:
            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2006",
                                      "obj": id})

                time.sleep(0.025)
                if "result" in i.current_message.keys():
                    response += i.current_message['result']

            for i in self.database.publicaciones.find({'id_usuario': id['id_usuario']}):
                aux = {'id_publicacion': i['id_publicacion'],
                       'id_usuario': i['id_usuario'],
                       'nombre': i['nombre'],
                       'descripcion': i['descripcion'],
                       'precio': i['precio'],
                       'categoria': i['categoria'],
                       'host': self.ip
                       # 'img_list':i['img_list']
                       }
                response += [aux]
                ar = []
                ids = []
                for i in response:
                    if i['id_publicacion'] not in ids:
                        ar.append(i)
                        ids.append(i['id_publicacion'])
                response = ar
            return {'response': response}

        except Exception as e:
            raise e

    def get_user_comment_by_user_id(self, id: dict) -> dict:
        try:
            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2007",
                                      "obj": id})

                time.sleep(0.025)
                if "result" in i.current_message.keys():
                    response += i.current_message['result']

            for i in self.database.comentariosusuario.find({'id_usuario': id['id_usuario']}):
                aux = {'id_comment': i['id_comment'],
                       'id_usuario': i['id_usuario'],
                       'encabezado': i['encabezado'],
                       'fecha_comentario': i['fecha_comentario'],
                       'puntuacion': i['puntuacion'],
                       'descripcion': i['descripcion']}
                response += [aux]
            ar = []
            ids = []
            for i in response:
                if i['id_comment'] not in ids:
                    ar.append(i)
                    ids.append(i['id_comment'])
            response = ar
            return {'response': response}

        except Exception as e:
            raise e

    def get_product_comment_by_product_id(self, id: dict) -> dict:
        try:
            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2008",
                                      "obj": id})

                time.sleep(0.025)
                if "result" in i.current_message.keys():
                    response += i.current_message['result']

            for i in self.database.comentariospublicacion.find({'id_publicacion': id['id_publicacion']}):
                aux = {'id_comment': i['id_comment'],
                       'id_usuario': i['id_usuario'],
                       "id_publicacion": i['id_publicacion'],
                       'encabezado': i['encabezado'],
                       'fecha_comentario': i['fecha_comentario'],
                       'puntuacion': i['puntuacion'],
                       'descripcion': i['descripcion']}
                response += [aux]
            ar = []
            ids = []
            for i in response:
                if i['id_comment'] not in ids:
                    ar.append(i)
                    ids.append(i['id_comment'])
            response = ar

            return {'response': response}

        except Exception as e:
            raise e

    def check_chat(self, chat: dict) -> dict:
        try:

            aux = {'response': '0'}
            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2009",
                                      "obj": id})

                time.sleep(0.025)
                if "result" in i.current_message.keys():
                    response += i.current_message['result']

            a = 0
            for i in self.database.chats.find({'user1_id': chat['user1_id'], 'user2_id': chat['user2_id']}):
                a += 1
            for i in self.database.chats.find({'user1_id': chat['user2_id'], 'user2_id': chat['user1_id']}):
                a += 1

            if a != 0:
                aux['response'] = '1'

            return aux

        except Exception as e:
            raise e

    def get_chat(self, chat: dict) -> dict:
        try:

            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2010",
                                      "obj": id})

                time.sleep(0.025)
                if "result" in i.current_message.keys():
                    response += i.current_message['result']

            for i in self.database.chats.find({'user1_id': chat['user1_id'], 'user2_id': chat['user2_id']}):
                aux = {'id_chat': i['id_chat'],
                       'user1_id': i['user1_id'],
                       'user2_id': i['user2_id'],
                       'message_list': i['message_list']}
                response += [aux]
            for i in self.database.chats.find({'user1_id': chat['user2_id'], 'user2_id': chat['user1_id']}):
                aux = {'id_chat': i['id_chat'],
                       'user1_id': i['user1_id'],
                       'user2_id': i['user2_id'],
                       'message_list': i['message_list']}
                response += [aux]

            return {"response": response}

        except Exception as e:
            raise e

    def get_all_user_chats(self, id: dict) -> dict:
        try:

            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2013",
                                      "obj": id})

                time.sleep(0.025)
                if "result" in i.current_message.keys():
                    response += i.current_message['result']

            for i in self.database.chats.find({'user1_id': id['id_usuario']}):
                aux = {'id_chat': i['id_chat'],
                       'user1_id': i['user1_id'],
                       'user2_id': i['user2_id'],
                       'message_list': i['message_list']}

                if len(i['message_list']) > 0:
                    aux['message_list'] = [
                        i['message_list'][len(i['message_list'])-1]]

                response += [aux]

            for i in self.database.chats.find({'user2_id': id['id_usuario']}):
                aux = {'id_chat': i['id_chat'],
                       'user1_id': i['user1_id'],
                       'user2_id': i['user2_id'],
                       'message_list': i['message_list']}

                if len(i['message_list']) > 0:
                    aux['message_list'] = [
                        i['message_list'][len(i['message_list'])-1]]

                response += [aux]

            return {"response": response}

        except Exception as e:
            raise e

    def get_chat_by_id(self, id: dict) -> dict:
        try:

            response = []
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2014",
                                      "obj": id})

                time.sleep(0.025)
                if "result" in i.current_message.keys():
                    response += i.current_message['result']

            for i in self.database.chats.find({'id_chat': id['id_chat']}):
                aux = {'id_chat': i['id_chat'],
                       'user1_id': i['user1_id'],
                       'user2_id': i['user2_id'],
                       'message_list': [i['message_list'][len(i['message_list'])-1]]}

                response += [aux]

            return {"response": response}

        except Exception as e:
            raise e

    def get_publicacion_random(self, length: int) -> dict:
        try:
            response = []
            object_list = []
            tope = int(length/(len(self.all_nodes)+1))
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "2012",
                                      "obj": tope})

                time.sleep(0.025)
                if "result" in i.current_message.keys():
                    object_list += i.current_message['result']

            for i in self.database.publicaciones.find({}):
                aux = {'id_publicacion': i['id_publicacion'],
                       'id_usuario': i['id_usuario'],
                       'nombre': i['nombre'],
                       'descripcion': i['descripcion'],
                       'precio': i['precio'],
                       'categoria': i['categoria'],
                       'host': self.ip
                       # 'img_list':i['img_list']
                       }
                object_list.append(aux)

            lo = len(object_list)

            if length > lo:
                length = lo

            i = 0
            response = []
            ids = []

            while (i < length):
                index = np.random.randint(lo)
                id = object_list[index]["id_publicacion"]
                if (id not in ids):
                    response.append(object_list[index])
                    ids.append(id)
                    i += 1

            return response

        except Exception as e:
            raise e

    def get_user_image(self, id: str) -> dict:

        lst = []
        for i in self.database.usuarios.find({'id_usuario': id}):
            lst.append(i['img_usuario'])

        if len(i) > 0:
            obj = lst[0]
            b64 = obj['file']
            # base64.decode(b64)
            return {'img': b64}

        else:
            return {"error"}

    def get_product_image(self, id: str) -> dict:

        lst = []
        for i in self.database.publicaciones.find({'id_publicacion': id}):
            lst.append(i['img_list'][0])

        if len(i) > 0:
            obj = lst[0]
            b64 = obj['file']

            return {'img': b64}

        else:
            return {'message': "error"}

    """ Uso de las modificaciones:
            La aplicación cliente envía un json con el sig. formato:
                {id_usuario/producto: id,
                 campos a modificar:{campos...}
                 }

    
    """

    def modify_product(self, obj: dict) -> dict:
        try:

            for i in self.all_nodes:
                self.send_to_node(i, {'message': '3001',
                                      'obj': obj})
            self.database.publicaciones.update_one(
                {"id_publicacion": obj['id_publicacion']}, {'$set': obj['campos']})

        except Exception as e:
            raise e

    def modify_user(self, obj: dict) -> dict:
        try:
            for i in self.all_nodes:
                self.send_to_node(i, {'message': '3002',
                                      'obj': obj})
            self.database.usuarios.update_one(
                {"id_usuario": obj['id_usuario']}, {'$set': obj['campos']})
        except Exception as e:
            raise e

    def insert_message(self, obj: dict) -> dict:
        try:

            for i in self.all_nodes:
                self.send_to_node(i, {'message': '3003',
                                      'obj': obj})

            chat = {}
            for i in self.database.chats.find({"id_chat": obj['id_chat']}):
                aux = {'id_chat': i['id_chat'],
                       'user1_id': i['user1_id'],
                       'user2_id': i['user2_id'],
                       'message_list': i['message_list']}
                chat = aux

            if len(chat.keys()) == 0:
                return {'message': '505'}
            else:

                lst = chat['message_list']
                lst.append(obj['message'])
                self.database.chats.update_one({"id_chat": obj['id_chat']}, {
                                               '$set': {'message_list': lst}})

                return {'message': '200'}
        except Exception as e:
            raise e

    def delete_product(self, id: dict):
        try:
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "4001",
                                      "obj": id})

            self.database.publicaciones.delete_one(
                {'id_publicacion': id['id_publicacion']})

        except Exception as e:
            raise e

    def delete_user(self, id: dict):
        try:
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "4002",
                                      "obj": id})

            self.database.usuarios.delete_one({'id_usuario': id['id_usuario']})

        except Exception as e:
            raise e

    def delete_chat(self, id: dict):
        try:
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "4003",
                                      "obj": id})

            self.database.chats.delete_one({'id_chat': id['id_chat']})

        except Exception as e:
            raise e

    def delete_post_comment(self, id: dict):
        try:
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "4004",
                                      "obj": id})

            self.database.comentariospublicacion.delete_one(
                {'id_comment': id['id_comment']})

        except Exception as e:
            raise e

    def delete_user_comment(self, id: dict):
        try:
            for i in self.all_nodes:

                self.send_to_node(i, {"message": "4005",
                                      "obj": id})

            self.database.comentariosusuario.delete_one(
                {'id_comment': id['id_comment']})

        except Exception as e:
            raise e

    def node_message(self, connected_node, data):
        self.debug_print("node_message from " +
                         connected_node.host + ": " + str(data))
        if (isinstance(data, dict) and "message" in data.keys()):

            if (data['message'] == "1001"):

                try:
                    obj = data['obj']
                    publicaciones = self.database['publicaciones']
                    result = self.database.publicaciones.insert_one(obj)
                    self.send_to_node(connected_node, result)

                except Exception as e:
                    self.debug_print(e)
                    raise e
            if (data['message'] == "1002"):
                try:
                    obj = data['obj']
                    usuarios = self.database['usuarios']
                    result = self.database.usuarios.insert_one(obj)
                    self.send_to_node(connected_node, result)

                except Exception as e:
                    self.debug_print(e)
                    raise e

            if (data['message'] == "1003"):
                try:
                    obj = data['obj']
                    comentariosusuario = self.database['comentariosusuario']
                    result = self.database.comentariosusuario.insert_one(obj)
                    self.send_to_node(connected_node, result)

                except Exception as e:
                    self.debug_print(e)
                    raise e

            if (data['message'] == "1004"):
                try:
                    obj = data['obj']
                    comentariospublicacion = self.database['comentariospublicacion']
                    result = self.database.comentariospublicacion.insert_one(
                        obj)
                    self.send_to_node(connected_node, result)

                except Exception as e:
                    self.debug_print(e)
                    raise e

            if data['message'] == "1005":
                try:
                    chat = data['obj']
                    result = self.database.chats.insert_one(chat)
                    self.send_to_node(connected_node, {'result': result})
                except Exception as e:
                    raise e

            if data['message'] == "1006":
                try:
                    obj = data['obj']
                    chat = {}
                    for i in self.database.chats.find({"id_chat": obj['id_chat']}):
                        aux = {'id_chat': i['id_chat'],
                               'user1_id': i['user1_id'],
                               'user2_id': i['user2_id'],
                               'message_list': i['message_list']}
                        chat = aux

                    if len(chat.keys()) == 0:
                        return {'message': '505'}
                    else:

                        lst = chat['message_list']
                        lst.append(obj['message'])
                        self.database.chats.update_one({"id_chat": obj['id_chat']}, {
                                                       '$set': {'message_list': lst}})

                        return {'message': '200'}
                except Exception as e:
                    raise e
                except Exception as e:
                    raise e
            if (data['message'] == "2001"):
                result = []
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
                               'zona_entrega_usuario': i['zona_entrega_usuario'],
                               'host': self.ip
                               # 'img_usuario':i['img_usuario']
                               }
                        result.append(aux)

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})
            if (data['message'] == "2002"):
                result = []
                try:
                    obj = data['obj']

                    resulta = self.database.usuarios.find(
                        {'nombre_usuario': {"$regex": obj, "$options": "i"}})

                    result = []
                    for i in resulta:
                        aux = {'id_usuario': i['id_usuario'],
                               'nombre_usuario': i['nombre_usuario'],
                               'contraseña_usuario': i['contraseña_usuario'],
                               'telefono_usuario': i['telefono_usuario'],
                               'correo_usuario': i['correo_usuario'],
                               'zona_entrega_usuario': i['zona_entrega_usuario'],
                               'host': self.ip
                               }
                        result.append(aux)

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})

            if (data['message'] == "2003"):
                result = []
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
                               'categoria': i['categoria'],
                               'host': self.ip
                               }
                        result.append(aux)

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})

            if (data['message'] == "2004"):
                result = []
                try:
                    obj = data['obj']

                    resulta = self.database.publicaciones.find(
                        {'nombre': {"$regex": obj, "$options": "i"}})

                    result = []
                    for i in resulta:
                        aux = {'id_usuario': i['id_usuario'],
                               'nombre_usuario': i['nombre_usuario'],
                               'contraseña_usuario': i['contraseña_usuario'],
                               'telefono_usuario': i['telefono_usuario'],
                               'correo_usuario': i['correo_usuario'],
                               'zona_entrega_usuario': i['zona_entrega_usuario'],
                               'host': self.ip
                               }
                        result.append(aux)

                except Exception as e:
                    raise e

                finally:
                    self.send_to_node(connected_node, {'result': result})

            if (data['message'] == "2005"):
                result = []
                try:

                    obj = data['obj']
                    publicaciones = self.database['publicaciones']

                    resulta = self.database.publicaciones.find(
                        {'categoria': {"$regex": obj, "$options": "i"}})

                    result = []
                    for i in resulta:
                        aux = {'id_publicacion': i['id_publicacion'],
                               'id_usuario': i['id_usuario'],
                               'nombre': i['nombre'],
                               'descripcion': i['descripcion'],
                               'precio': i['precio'],
                               'categoria': i['categoria'],
                               'host': self.ip
                               }
                        result.append(aux)

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})

            if (data['message'] == "2006"):
                result = []
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
                               'categoria': i['categoria'],
                               'host': self.ip
                               }
                        result.append(aux)

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})

            if (data['message'] == "2007"):
                result = []
                try:
                    obj = data['obj']
                    comentariosusuario = self.database['comentariosusuario']

                    resulta = self.database.comentariosusario.find(
                        {'id_usuario': obj['id_usuario']})

                    result = []
                    for i in resulta:
                        aux = {'id_comment': i['id_comment'],
                               'id_usuario': i['id_usuario'],
                               'encabezado': i['encabezado'],
                               'fecha_comentario': i['fecha_comentario'],
                               'puntuacion': i['puntuacion'],
                               'descripcion': i['descripcion']}
                        result.append(aux)

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})

            if (data['message'] == "2008"):
                result = []
                try:
                    obj = data['obj']
                    comentariospublicacion = self.database['comentariospublicacion']

                    resulta = self.database.comentariospublicacion.find(
                        {'id_publicacion': obj['id_publicacion']})

                    result = []
                    for i in resulta:
                        aux = {'id_comment': i['id_comment'],
                               'id_usuario': i['id_usuario'],
                               "id_publicacion": i['id_publicacion'],
                               'encabezado': i['encabezado'],
                               'fecha_comentario': i['fecha_comentario'],
                               'puntuacion': i['puntuacion'],
                               'descripcion': i['descripcion']}
                        result.append(aux)

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})
            if (data['message'] == "2009"):
                result = []
                try:

                    a = 0
                    chat = data['obj']
                    for i in self.database.chats.find({'user1_id': chat['user1_id'], 'user2_id': chat['user2_id']}):
                        a += 1
                    for i in self.database.chats.find({'user1_id': chat['user2_id'], 'user2_id': chat['user1_id']}):
                        a += 1

                    if a != 0:
                        aux['response'] = '1'

                    result = aux['response']

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})
            if (data['message'] == "2010"):
                response = []
                try:
                    chat = data['obj']
                    response = []

                    for i in self.database.chats.find({'user1_id': chat['user1_id'], 'user2_id': chat['user2_id']}):
                        response += [i]
                    for i in self.database.chats.find({'user1_id': chat['user2_id'], 'user2_id': chat['user1_id']}):
                        response += [i]

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': response})

            if data['message'] == "2011":
                result = []
                try:
                    obj = data['obj']
                    usuarios = self.database['usuarios']

                    resulta = self.database.usuarios.find(
                        {'correo_usuario': obj})

                    result = []
                    for i in resulta:
                        aux = {'id_usuario': i['id_usuario'],
                               'nombre_usuario': i['nombre_usuario'],
                               'contraseña_usuario': i['contraseña_usuario'],
                               'telefono_usuario': i['telefono_usuario'],
                               'correo_usuario': i['correo_usuario'],
                               'zona_entrega_usuario': i['zona_entrega_usuario'],
                               'host': self.ip
                               }
                        result.append(aux)

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})

            if data['message'] == '2012':
                length = 3
                print("Mandando publicacion random...")
                result = []
                print(length)
                try:
                    j = 0
                    lst = []
                    for i in self.current_post:
                        aux = {'id_publicacion': i['id_publicacion'],
                               'id_usuario': i['id_usuario'],
                               'nombre': i['nombre'],
                               'descripcion': i['descripcion'],
                               'precio': i['precio'],
                               'categoria': i['categoria'],
                               'host': self.ip
                               }
                        result.append(aux)
                        j += 1
                        if j == length:
                            break

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})

            if data['message'] == "2013":
                response = []
                id = data['obj']
                try:
                    for i in self.database.chats.find({'id_usuario': id['user1_id']}):
                        aux = {'id_chat': i['id_chat'],
                               'user1_id': i['user1_id'],
                               'user2_id': i['user2_id'],
                               'message_list': [i['message_list'][len(i['message_list'])-1]]}
                        response.append(aux)

                        response += [aux]
                    for i in self.database.chats.find({'id_usuario': id['user2_id']}):
                        aux = {'id_chat': i['id_chat'],
                               'user1_id': i['user1_id'],
                               'user2_id': i['user2_id'],
                               'message_list': i['message_list'][len(i['message_list'])-1]}
                        response += [aux]

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': response})
            if data['message'] == '2014':

                id = data['obj']
                response = []
                try:
                    for i in self.database.chats.find({'id_chat': id['id_chat']}):
                        aux = {'id_chat': i['id_chat'],
                               'user1_id': i['user1_id'],
                               'user2_id': i['user2_id'],
                               'message_list': [i['message_list'][len(i['message_list'])-1]]}

                        response += [aux]

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': response})

            if (data['message'] == '3001'):
                result = []
                try:
                    obj = data['obj']

                    publicaciones = self.database['publicaciones']
                    result = self.database.publicaciones.update_one(
                        {"id_publicacion": obj['id_publicacion']}, {'$set': obj['campos']})

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})
            if (data['message'] == '3002'):
                result = []
                try:
                    obj = data['obj']

                    usuarios = self.database['usuarios']
                    result = self.database.usuarios.update_one(
                        {"id_usuario": obj['id_usuario']}, {'$set': obj['campos']})

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})

            if data['message'] == '3003':
                result = []
                try:
                    obj = data['obj']
                    chat = {}
                    for i in self.database.chats.find({"id_chat": obj['id_chat']}):
                        aux = {'id_chat': i['id_chat'],
                               'user1_id': i['user1_id'],
                               'user2_id': i['user2_id'],
                               'message_list': i['message_list']}
                        chat = aux

                    if len(chat.keys()) == 0:
                        self.send_to_node(connected_node, {'result': '505'})
                    else:

                        lst = chat['message_list']
                        lst.append(obj['message'])
                        result = self.database.chats.update_one({"id_chat": obj['id_chat']}, {
                                                                '$set': {'message_list': lst}})

                except Exception as e:
                    raise e
                finally:
                    self.send_to_node(connected_node, {'result': result})

            if (data['message'] == '4001'):
                try:
                    id = data['obj']
                    self.database.publicaciones.delete_one(
                        {'id_publicacion': id['id_publicacion']})
                except Exception as e:
                    raise e
            if (data['message'] == '4002'):
                try:
                    id = data['obj']
                    self.database.usuarios.delete_one(
                        {'id_usuario': id['id_usuario']})
                except Exception as e:
                    raise e

            if (data['message'] == '4003'):
                try:
                    id = data['obj']
                    self.database.chats.delete_one({'id_chat': id['id_chat']})
                except Exception as e:
                    raise e

            if (data['message'] == '4004'):
                try:
                    id = data['obj']
                    self.database.comentariospublicacion.delete_one(
                        {'id_comment': id['id_comment']})
                except Exception as e:
                    raise e

            if (data['message'] == '4005'):
                try:
                    id = data['obj']
                    self.database.comentariosusuario.delete_one(
                        {'id_comment': id['id_comment']})
                except Exception as e:
                    raise e
            if data['message'] == "666":
                self.debug_print(f"Node disconnected: {connected_node.host}")
                self.disconnect_with_node(connected_node)

    def inbound_node_connected(self, node: NodeConnection):
        self.debug_print(f"Inbound node connected {node.host}:{node.port}")
        for i in self.nodes_inbound:
            lst = []
            if i.host != node.host:
                self.send_to_node(i, {'message': "7778",
                                      'obj': f'{node.host}:{node.port}'})
                lst.append(f"{i.host}:{i.port}")
            self.send_to_node(node, {'message': "7777", "obj": lst})

    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: ")

    def node_request_to_stop(self):
        print("node is requested to stop!")
