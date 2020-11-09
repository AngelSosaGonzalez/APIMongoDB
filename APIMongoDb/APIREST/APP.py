#Importamos Flask
from flask import Flask, request, jsonify, Response

#Importamos PyMongo 
import pymongo
from flask_pymongo import PyMongo

#Importamos DNS
import dns

#Importamos BSON
from bson import json_util

#Importacion de Object id
from bson.objectid import ObjectId

#Nunca dije esto, pero esta liena de codigo sirve para la creacion de nuestro API
app = Flask(__name__)

#Aqui vamos a arrancar nuestra API, comenzaremos con la conexion
app.config['MONGO_URI'] = "*Enalece de MongoDBAtlas*"

#Pediomos los recursos por medio de pymongo
API = PyMongo(app)

#Creacion de rutas
#En lo personal ya me canse un poco de pensar un nombre asi que sera en la pagina inicial 
#del localhost

#Ingresar ususario o documentos como le quieras llamar
@app.route('/', methods = ['POST'])
def POSTperfil():
    Nombre = request.json['Nombre']
    Edad = request.json['Edad']
    Ciudad = request.json['Ciudad']

    #Vamos a usar la comprobacion de envio
    if Nombre and Edad and Ciudad:
        #Vamos a crear la base de datos y la coleccion
        id = API.db.perfil.insert({
            'Nombre': Nombre,
            'Edad': Edad,
            'Ciudad': Ciudad
        })

        usuario = {
            'id': str(id),
            'Nombre': Nombre,
            'Edad': Edad,
            'Ciudad': Ciudad 
        }
        return usuario
    else:
        return NoHayServicio()

#Listado de los datos
@app.route('/Usuarios')
def GETperfiles():
    #Aqui nos dara los datos perooo... en formato BSON y no queremos esto
    usuarios =  API.db.perfil.find()
    #Aqui es donde entra el modulo BSON que lo convierte en Json 
    perfiles = json_util.dumps(usuarios)
    #Aqui enviamos los resultados
    return Response(perfiles, mimetype='application/json')

#Ahora vamos a buscar un usuario en especifico
@app.route('/Usuario/<id>')
def GETperfilunic(id):
    #Aqui nos dara los datos perooo... en formato BSON y no queremos esto
    usuarios =  API.db.perfil.find_one({'_id':ObjectId(id)})
    #Aqui es donde entra el modulo BSON que lo convierte en Json 
    perfiles = json_util.dumps(usuarios)
    #Aqui enviamos los resultados 
    return Response(perfiles, mimetype='application/json')

#Eliminar datos
@app.route('/<id>', methods = ['DELETE'])
def DELETEperfil(id):
    #Esta linea de codigo vamos a eliminar el dato
    API.db.perfil.delete_one({'_id':ObjectId(id)})
    #Mensaje que dara al eliminar
    Mensaje = jsonify({'Mensaje': 'Te quebraste al ' + id})
    #Confirmacion
    return Mensaje

#Actualizar datos
@app.route('/Usuarios/<id>', methods = ['PUT'])
def PUTperfil(id):
    Nombre = request.json['Nombre']
    Edad = request.json['Edad']
    Ciudad = request.json['Ciudad']

    #Actualizar los datos
    if Nombre and Edad and Ciudad:
        API.db.perfil.update_one({'_id':ObjectId(id)}, {'$set': {
            'Nombre': Nombre,
            'Edad': Edad,
            'Ciudad': Ciudad
        }})
        #Mensaje de confirmacion
        mensaje = jsonify({'Mensaje': 'QUE HICISTE, PORQUE CAMBIASTE LOS DATOS DE: ' + id})
        return mensaje


#Crearemos un mensaje de error igual que 404 (bueno no igual, haremos nuestro 404)
@app.errorhandler(404)
def NoHayServicio(error=None):
    mensaje = jsonify({
        'mensaje': 'Hijole joven no hay servicio, le atendemos en la otra caja ' + request.url,
        'ERROR': 'Te cayo el 404 mi chavo'
    })
    mensaje.status_code = 404
    return mensaje

#Arranacamos nuestra API asi:
#Enun futuro se me va a olvidar, recuerda que debug = True, sirve cuando realizamos cambios
#al codigo de esta API se reinicia para correr con los cambios dados
if __name__ == "__main__":
    app.run(debug=True)
