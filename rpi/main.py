'''
 1 Escuchar mensajes MQTT (listo)
 El mensaje es del tipo JSON 
 2 Guardar datos en archivo CSV
 3 Valida conexion a internet 
     si no hay, guardar datos en TXT de respaldo
     Si hay y el TXT de respaldo no tiene dato, descomponer mensaje y acomodarlo a la estructura para Firebase y enviarlos.
     Si hay y el TXT de respaldo tiene datos, recorrer el CSV y enviar los datos a firebase
'''

import ssl
import sys
import paho.mqtt.client as mqtt
import txtFile
import csvFile
import timeData
import conection
import backupData
import firebase
 
def on_connect(client, userdata, flags, rc):
    print('connected (%s)' % client._client_id)
    client.subscribe(topic='invernadero/#', qos=2)
 
def on_message(client, userdata, message):
    # ======================================================
    print('------------------------------')
    # Descomponer topic para obtener locacion e ID del dispositivo
    auxTopic = message.topic.split(":")
    # Descomponer mensaje para obtener temperatura y humedad
    auxMessage = message.payload.split("/")
    # Crear diccionario con informacion a almacenar
    dataCurrent = {
        'id': int(auxTopic[1]),
        'position': str(auxTopic[0]),
        'timestamp': timeData.getTimestamp(),
        'tem': int(auxMessage[0]),
        'hum': int(auxMessage[1])
    }
    print dataCurrent

    # ======================================================
    # Obtener informacion sobre archivo de respaldo
    dataBack = txtFile.getDate()
    # Crear nuevo archivo si no hay datos creados o la fecha actual es diferente a la fecha almacenada
    if len(dataBack) == 0 or dataBack[0] != timeData.getCurrentDateSTR():
        # Escribir datos de dataCurrent en archivo CSV creado
        csvFile.createFile(txtFile.newDay(timeData.getCurrentDateSTR()),dataCurrent)
    # en caso contrario, escribir el dato en el archivo CSV.
    else:
        # Escribir datos de dataCurrent en CSV
        csvFile.writeData(dataBack[1], dataCurrent)

    # ======================================================
    # Validar conexion a internet, si no hay, se almacena el mensaje en backup de respaldo
    if conection.valid():
        # Enviar dato a firebase
        firebase.save(dataCurrent)
        # revisar si existen datos en archivo de respaldo
        lis = backupData.loadBackup()
        if lis != False:
            # Recorrer array con datos y almacenarlos en firebase
            for i in lis:
                firebase.save(i)
    else:
        # almacenar dato de respaldo
        backupData.saveBackup(dataCurrent)

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(host='192.168.1.123', port=1883)
client.loop_forever()