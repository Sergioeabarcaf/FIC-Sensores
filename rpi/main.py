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
 
def on_connect(client, userdata, flags, rc):
    print('connected (%s)' % client._client_id)
    client.subscribe(topic='invernadero/#', qos=2)
 
def on_message(client, userdata, message):
    print('------------------------------')
    print('topic: %s' % message.topic)
    print('payload: %s' % message.payload)
    print(client)
    auxMessage = message.payload.split("/")
    dataCurrent = {
        'position': str(message.topic),
        'timestamp': timeData.getTimestamp(),
        'temp': auxMessage[0],
        'hum': auxMessage[1]
    }
    print dataCurrent
    dataBack = txtFile.getDate()
    # Crear nuevo archivo si no hay datos creados o la fecha actual es diferente a la fecha almacenada
    if len(dataBack) == 0 or dataBack[0] != timeData.getCurrentDateSTR():
        csvFile.createFile(txtFile.newDay(timeData.getCurrentTimeSTR()),message.payload)
    # en caso contrario, escribir el dato en el archivo CSV.
    else:
        csvFile.writeData(dataBack[1], message.payload)


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(host='192.168.1.123', port=1883)
client.loop_forever()