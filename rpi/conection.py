import socket

def valid():
    test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        test.connect(('www.google.com',80))
        test.close()
        return True
    except:
        test.close()
        return False