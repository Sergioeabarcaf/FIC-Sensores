import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

cred = credentials.Certificate('./testInvernadero.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fic-testinvernadero.firebaseio.com/'
})

# Funcion que almacena un nuevo dato en Firebase
def save(data):
    # la direccion a almacenar es de tipo invernadero/espacio/id
    dir = 'data/' + str(data["position"]) + "/id" + str(data["id"])
    db.reference(dir).push(data)
