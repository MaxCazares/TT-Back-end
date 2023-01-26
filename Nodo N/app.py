from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from Centralpeer.CentralPeer import CentralPeer
import signal
import time
from base64 import b64decode
from io import BytesIO
import re


def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


port = 2323

while (is_port_in_use(port) == True):
    port += 1

centralpeer = CentralPeer('0.0.0.0', port)
centralpeer.start()
centralpeer.connect_with_node("20.150.141.5", 2323, reconnect=True)

app = Flask(__name__)


def handler(signum, frame):
    msg = "\n\n\nApagando nodo, desconectando superpares\n\n\tEspere..."
    print(msg)
    for i in centralpeer.all_nodes:
        centralpeer.send_to_node(i, {"message": "666"})
    centralpeer.stop()
    print("Adios")
    time.sleep(1)
    exit(1)


signal.signal(signal.SIGINT, handler)


@app.route('/')
@cross_origin()
def hello():
    return "<h1 style='color:blue'>Quick</h1><br><h1 style='color:yellow'>         Shop</h1>"


def page_not_found(error):
    return "<h1>Error</h1>", 404


@app.route('/usuarios/getbyid/<id>', methods=['GET'])
@cross_origin()
def get_user_id(id):
    result = centralpeer.get_user_by_id({"id_usuario": id})
    return jsonify(result)


@app.route('/usuarios/getbyname/<nombre>', methods=['GET'])
@cross_origin()
def get_user_nombre(nombre):
    result = centralpeer.get_user_by_name({"nombre": nombre})
    return jsonify(result)


@app.route('/usuarios/getbyemail/<email>', methods=['GET'])
@cross_origin()
def get_user_by_email(email):
    result = centralpeer.get_user_by_email({"email": email})
    return jsonify(result)


@app.route('/usuarios', methods=['POST'])
@cross_origin()
def insert_user():

    aux = {'id_usuario': centralpeer.generate_id(),
           'nombre_usuario': request.json['nombre_usuario'],
           'contraseña_usuario': request.json['contraseña_usuario'],
           'telefono_usuario': request.json['telefono_usuario'],
           'correo_usuario': request.json['correo_usuario'],
           'zona_entrega_usuario': request.json['zona_entrega_usuario'],
           'img_usuario': request.json['img_usuario']}

    centralpeer.insert_user(aux)
    return jsonify({'message': 'Usuario Insertado'})


@app.route("/usercomment", methods=["POST"])
@cross_origin()
def insert_user_comment():
    aux = {'id_comment': centralpeer.generate_id(),
           'id_usuario': request.json['id_usuario'],
           'encabezado': request.json['encabezado'],
           'fecha_comentario': request.json['fecha_comentario'],
           'puntuacion': request.json['puntuacion'],
           'descripcion': request.json['descripcion']}

    centralpeer.insert_user_comment(aux)

    return jsonify({'message': 'Comentario de Usuario Insertado'})


"""
    {"id_comment":centralpeer.generate_id(),
           "id_usuario":request.json["id_usuario"],
           "id_publicacion":request.json["id_publicacion"],
           "encabezado":request.json["encabezado"],
           "fecha_comentario":request.json["fecha_comentario"],
           "puntuacion":request.json["puntuacion"],
           "descripcion":request.json["descripcion"]}

"""


@app.route("/usercomment/getbyuserid/<id>", methods=["GET"])
@cross_origin()
def get_user_comment_by_user_id(id):

    result = centralpeer.get_user_comment_by_user_id({"id_usuario": id})

    return jsonify(result)


@app.route("/postcomment", methods=["POST"])
@cross_origin()
def insert_post_comment():
    aux = {'id_comment': centralpeer.generate_id(),
           'id_usuario': request.json['id_usuario'],
           "id_publicacion": request.json['id_publicacion'],
           'encabezado': request.json['encabezado'],
           'fecha_comentario': request.json['fecha_comentario'],
           'puntuacion': request.json['puntuacion'],
           'descripcion': request.json['descripcion']}

    centralpeer.insert_post_comment(aux)

    return jsonify({'message': 'Comentario de Publicacion Insertado'})


@app.route("/postcomment/getbypostid/<id>", methods=["GET"])
@cross_origin()
def get_post_comment_by_product_id(id):
    result = centralpeer.get_product_comment_by_product_id(
        {"id_publicacion": id})

    return jsonify(result)


@app.route('/publicaciones/getbyid/<id>', methods=['GET'])
@cross_origin()
def get_publicacion_id(id):
    result = centralpeer.get_product_by_id({"id_publicacion": id})
    return jsonify(result)


@app.route('/publicaciones/getbyuserid/<id>', methods=["GET"])
@cross_origin()
def get_publicacion_id_usuario(id):
    result = centralpeer.get_product_by_user_id({'id_usuario': id})
    return jsonify(result)


@app.route('/publicaciones/getbyname/<nombre>', methods=['GET'])
@cross_origin()
def get_publicacion_nombre(nombre):
    result = centralpeer.get_product_by_name({"nombre": nombre})
    return jsonify(result)


@app.route('/publicaciones/getrandom', methods=["GET"])
@cross_origin()
def get_publicacion_random():

    result = centralpeer.get_publicacion_random(12)

    return jsonify({"response": result})


@app.route('/publicaciones/getbycategory/<categoria>', methods=['GET'])
@cross_origin()
def get_publicacion_categoria(categoria):
    result = centralpeer.get_product_by_category({"categoria": categoria})
    return jsonify(result)


@app.route('/publicaciones', methods=['POST'])
@cross_origin()
def insert_publicacion():

    aux = {'id_publicacion': centralpeer.generate_id(),
           'nombre': request.json['nombre'],
           'id_usuario': request.json['id_usuario'],
           'descripcion': request.json['descripcion'],
           'precio': request.json['precio'],
           'categoria': request.json['categoria'],
           'img_list': request.json['img_list']}

    centralpeer.insert_product(aux)
    centralpeer.add_random_prod(aux)

    return jsonify({'message': 'Producto Insertado'})


@app.route('/usuarios/update', methods=['PUT'])
@cross_origin()
def update_usuario():
    id = request.json['id']
    aux = request.json['campos']
    campos = {'nombre_usuario': aux['nombre_usuario'],
              'contraseña_usuario': aux['contraseña_usuario'],
              'telefono_usuario': aux['telefono_usuario'],
              'correo_usuario': aux['correo_usuario'],
              'zona_entrega_usuario': aux['zona_entrega_usuario'],
              'img_usuario': aux['img_usuario']}

    centralpeer.modify_user({"id_usuario": id, 'campos': campos})

    return jsonify({'message': 'Usuario Modificado'})


@app.route('/publicaciones/update', methods=['PUT'])
@cross_origin()
def update_publicacion():

    id = request.json['id']
    aux = request.json['campos']
    campos = {'nombre': aux['nombre'],
              'id_usuario': aux['id_usuario'],
              'precio': aux['precio'],
              "descripcion": aux['descripcion'],
              'categoria': aux['categoria'],
              'img_list': aux['img_list']}

    centralpeer.modify_product({"id_publicacion": id, 'campos': campos})
    return jsonify({'message': "Publicacion Modificada"})


@app.route('/publicaciones/<id>', methods=['DELETE'])
@cross_origin()
def delete_publicacion(id):
    centralpeer.delete_product({"id_publicacion": id})
    return jsonify({'message': 'Publicacion eliminada!'})


@app.route('/usuarios/<id>', methods=['DELETE'])
@cross_origin()
def delete_usuario(id):
    centralpeer.delete_user({"id_usuario": id})

    return jsonify({'message': 'Usuario eliminado!'})


@app.route('/postcomment/<id>', methods=['DELETE'])
@cross_origin()
def delete_post_comment(id):
    centralpeer.delete_post_comment({"id_comment": id})
    return jsonify({"message": "Comentario eliminado!"})


@app.route('/usercomment/<id>', methods=['DELETE'])
@cross_origin()
def delete_user_comment(id):
    centralpeer.delete_usert_comment({"id_comment": id})
    return jsonify({"message": "Comentario eliminado!"})


""" 
---------------------------------    Bloque de codigo correspondiente al chat ------------------------------------
"""


@app.route('/chat/', methods=['POST'])
@cross_origin()
def create_chat():
    aux = {'id_chat': centralpeer.generate_id(),
           'user1_id': request.json['user1_id'],
           'user2_id': request.json['user2_id'],
           'message_list': []}
    centralpeer.create_chat(aux)
    return jsonify({'message': 'chat creado'})


@app.route('/chat/check/<both_ids>', methods=['GET'])
@cross_origin()
def check_chat(both_ids):

    user1_id = both_ids.split(";")[0]
    user2_id = both_ids.split(";")[1]
    aux = {'user1_id': user1_id,
           'user2_id': user2_id}

    response = centralpeer.check_chat(aux)

    return jsonify(response)


@app.route('/chat/getchat/<both_ids>', methods=['GET'])
@cross_origin()
def get_chat(both_ids):
    user1_id = both_ids.split(";")[0]
    user2_id = both_ids.split(";")[1]
    aux = {'user1_id': user1_id,
           'user2_id': user2_id}

    response = centralpeer.get_chat(aux)

    return jsonify(response)


@app.route('/chat/insert_message', methods=['POST'])
@cross_origin()
def insert_message():
    aux = {'id_chat': request.json['id_chat'],
           'message': request.json['message']}

    response = centralpeer.insert_message(aux)

    return jsonify(response)


@app.route('/chat/getalluserchats/<id>', methods=['GET'])
@cross_origin()
def get_all_user_chats(id):
    response = centralpeer.get_all_user_chats({'id_usuario': id})
    return jsonify(response)


@app.route('/chat/getbychatid/<id>', methods=['GET'])
@cross_origin()
def get_chat_by_id(id):
    response = centralpeer.get_chat_by_id({'id_chat': id})

    return jsonify({'response': response})


@app.route('/chat/<id>', methods=['DELETE'])
@cross_origin()
def delete_chat(id):

    centralpeer.delete_chat({'id_chat': id})
    return jsonify({'message': "Chat eliminado"})


@app.route('/usuarios/getimage/<id>')
@cross_origin()
def get_user_image(id):
    result = centralpeer.get_user_image(id)

    if 'message' not in result.keys():

        return result["img"]

    return result


@app.route('/publicaciones/getimage/<id>')
@cross_origin()
def get_product_image(id):
    result = centralpeer.get_product_image(id)

    if 'message' not in result.keys():

        return result["img"]

    return result


if __name__ == '__main__':

    app.register_error_handler(404, page_not_found)
    app.run()
