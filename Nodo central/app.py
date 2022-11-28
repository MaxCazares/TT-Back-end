from flask import Flask, jsonify, request
from flask_cors import CORS
from Centralpeer.CentralPeer import CentralPeer


centralpeer = CentralPeer('0.0.0.0', 2323)

app = Flask(__name__)


def page_not_found(error):
    return "<h1>Buenas tardes, chingue usted a su madre</h1>", 404


@app.route('/usuarios/getbyid/<id>', methods=['GET'])
def get_user_id(id):
    result = centralpeer.get_user_by_id({"id_usuario": id})
    return jsonify(result)


@app.route('/usuarios/getbyname/<nombre>', methods=['GET'])
def get_user_nombre(nombre):
    result = centralpeer.get_user_by_name({"nombre": nombre})
    return jsonify(result)


@app.route('/usuarios', methods=['POST'])
def insert_user():

    aux = {'id_usuario': centralpeer.generate_id(),
           'nombre_usuario': request.json['nombre_usuario'],
           'contraseña_usuario': request.json['contraseña_usuario'],
           'telefono_usuario': request.json['telefono_usuario'],
           'correo_usuario': request.json['correo_usuario'],
           'zona_entrega_usuario': request.json['zona_entrega_usuario']}

    centralpeer.insert_user(aux)
    return jsonify({'message': 'Usuario Insertado'})


@app.route('/publicaciones/getbyid/<id>', methods=['GET'])
def get_publicacion_id(id):
    result = centralpeer.get_product_by_id({"id_publicacion": id})
    return jsonify(result)


@app.route('/publicaciones/getbyuserid/<id>', methods=["GET"])
def get_publicacion_id_usuario(id):
    result = centralpeer.get_product_by_user_id({'id_usuario': id})
    return jsonify(result)


@app.route('/publicaciones/getbyname/<nombre>', methods=['GET'])
def get_publicacion_nombre(nombre):
    result = centralpeer.get_product_by_name({"nombre": nombre})
    return jsonify(result)


@app.route('/publicaciones/getbycategory/<categoria>', methods=['GET'])
def get_publicacion_categoria(categoria):
    result = centralpeer.get_product_by_category({"categorias": categoria})
    return jsonify(result)


@app.route('/publicaciones', methods=['POST'])
def insert_publicacion():

    aux = {'id_publicacion': centralpeer.generate_id(),
           'nombre': request.json['nombre'],
           'id_usuario': request.json['id_usuario'],
           'descripcion': request.json['descripcion'],
           'precio': request.json['precio'],
           'categorias': request.json['categorias']}

    centralpeer.insert_product(aux)
    return jsonify({'message': 'Producto Insertado'})


@app.route('/usuarios/update', methods=['PUT'])
def update_usuario():
    id = request.json['id']
    aux = request.json['campos']
    campos = {'nombre_usuario': aux['nombre_usuario'],
              'contraseña_usuario': aux['contraseña_usuario'],
              'telefono_usuario': aux['telefono_usuario'],
              'correo_usuario': aux['correo_usuario'],
              'zona_entrega_usuario': aux['zona_entrega_usuario']}

    centralpeer.modify_user({"id_usuario": id, 'campos': campos})

    return jsonify({'message': 'Usuario Modificado'})


@app.route('/publicaciones/update', methods=['PUT'])
def update_publicacion():

    id = request.json['id']
    aux = request.json['campos']
    campos = {'nombre': aux['nombre'],
              'id_usuario': aux['id_usuario'],
              'precio': aux['precio'],
              "descripcion": aux['descripcion'],
              'categorias': aux['categorias']}

    centralpeer.modify_product({"id_publicacion": id, 'campos': campos})
    return jsonify({'message': "Publicacion Modificada"})


@app.route('/publicaciones/<id>', methods=['DELETE'])
def delete_publicacion(id):
    centralpeer.delete_product({"id_publicacion": id})

    return jsonify({'message': 'Publicacion eliminada!'})


@app.route('/usuarios/<id>', methods=['DELETE'])
def delete_usuario(id):
    centralpeer.delete_user({"id_usuario": id})

    return jsonify({'message': 'Usuario eliminado!'})


if __name__ == '__main__':
    centralpeer.start()
    app.register_error_handler(404, page_not_found)
    app.run()
