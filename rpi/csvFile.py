import csv

fieldNames = ['id', 'position', 'timestamp', 'T°', 'H°']

# Crear nuevo archivo de datos CSV y almacenar nuevos datos.
def createFile(nameFile, data):
    # Generar archivo y escribir las cabeceras 
    with open(nameFile, 'a') as csvfile:
        write = csv.DictWriter(csvfile, fieldnames = fieldNames)
        write.writeheader()
        # Escirbir los datos recibidos.
        write.writerow(data)

# Escirbir datos en archivo generado
def writeData(nameFile, data):
    # Abrir archivos y cargar los datos
    with open(nameFile, 'a') as csvfile:
        write = csv.DictWriter(csvfile, fieldnames = fieldNames)
        write.writerow(data)