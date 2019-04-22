'''
 1 Escuchar mensajes MQTT
 El mensaje es del tipo id/timestamp/temperatura/humedad
 2 Guardar datos en archivo CSV
 3 Valida conexion a internet 
     si no hay, guardar datos en TXT de respaldo
     Si hay y el TXT de respaldo no tiene dato, descomponer mensaje y acomodarlo a la estructura para Firebase y enviarlos.
     Si hay y el TXT de respaldo tiene datos, recorrer el CSV y enviar los datos a firebase
'''

import ssl
import sys
 
import paho.mqtt.client as mqtt
 
def on_connect(client, userdata, flags, rc):
    print('connected (%s)' % client._client_id)
    client.subscribe(topic='invernadero/#', qos=2)
 
def on_message(client, userdata, message):
    print('------------------------------')
    print('topic: %s' % message.topic)
    print('payload: %s' % message.payload)
    print('qos: %d' % message.qos)

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(host='192.168.1.123', port=1883)
client.loop_forever()