import datetime
import time

# Retornar timestamp actual
def getTimestamp():
    return time.time()

# Retornar Date en formato ddmmaaaa
def getCurrentDateSTR():
    return time.strftime('%d%m%Y')