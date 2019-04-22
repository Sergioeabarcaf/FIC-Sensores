# Abrir archivo de respaldo y consultar fecha y nombre
def getDate():
    # Almacenar en array data [date:xxxx, name:yyyy]
    data = []
    # Abrir archivo y recorrer sus dos lineas para agregarlas a data
    f = open("back.txt")
    for line in f:
        data.append(line)
    # Cerrar f y retornar data con valores.
    f.close()
    return data

# Actualizar datos de respaldo con nueva fecha y nuevo nombre
# variable date en formato ddmmaaaa
def newDay(date):
    # Generar nombre del archivo a trabajar.
    name = "testSensores_" + str(date) + ".csv\n"
    # Abrir archivo de respaldo y actualizar información
    f = open("back.txt","w")
    f.write("date:" + str(date) + "\n")
    f.write("name:" + name)
    # Cerrar archivo y retornar nombre para almacenar sensores
    f.close()
    return name