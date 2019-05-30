import os.path

# Abrir archivo de respaldo y consultar fecha y nombre
def getDate():
    # Almacenar en array data [date, name]
    data = []
    # Verificar que existe el archivo de respaldo
    path = "back.txt"
    if(os.path.isfile(path)):
        # Abrir archivo y recorrer sus dos lineas para agregarlas a data
        f = open("./back.txt")
        for line in f:
            # Eliminar los saltos de lineas.
            data.append(str(line).replace("\n",""))
        # Cerrar f y retornar data con valores.
        f.close()
    return data

# Actualizar datos de respaldo con nueva fecha y nuevo nombre
# variable date en formato ddmmaaaa
def newDay(date):
    # Generar nombre del archivo a trabajar.
    name = "testSensores_" + str(date) + ".csv"
    # Abrir archivo de respaldo y actualizar informacion
    f = open("back.txt","w")
    f.write(str(date) + "\n")
    f.write(name + "\n")
    # Cerrar archivo y retornar nombre para almacenar sensores
    f.close()
    return name

# Funcion para almacenar los log de errores con su timestamp
def logError(timestamp, type, arg):
    f = open("logError.txt","a")
    line = str(timestamp) + " - " + str(type) + " - " + str(arg)
    f.write(line + "\n")
    f.close()
    return True