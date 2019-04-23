import json
import os.path

path = "./backup.txt"

# Funcion para almacenar datos de respaldo
def saveBackup(data):
    # Abrir archivo de respaldo y almacenar data en formato string
    f = open(path, "w")
    # Flags para testeo
    print data
    print type(data)
    print json.dumps(data)
    f.write(json.dumps(data) + "\n")
    f.close()

# Funcion para revisar si existen datos en el archivo
def loadBackup():
    # Verificar si existe el archivo, si no existe el archivo, retornar False
    if os.path.isfile(path):
        # abrir el archivo y almacenar en un array los datos en formato json
        data = []
        f = open(path)
        for line in f:
            # Eliminar los saltos de linea de cada dato y convertirlos a json
            data.append(json.loads(str(line).replace("\n","")))
        f.close()
        # validar el largo de los datos antes de responder, si esta vacio, retornar false
        if len(data) > 0:
            print data
            return data
        else:
            return False
    else:
        return False
