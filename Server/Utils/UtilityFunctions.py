import json
import socket
from datetime import datetime


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip_address = s.getsockname()[0]
    except socket.error:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address


def object_to_bytes(object_to_send):
    return str.encode(json.dumps(object_to_send.__dict__))


def bytes_to_object(bytes_received):
    return json.loads(bytes_received)


def get_message_type(bytes_received):
    return json.loads(bytes_received)["TYPE"]


def log(message):
    now = datetime.now()
    print(str(now.strftime('%Y-%m-%d %H:%M:%S')), end="")
    print(message)
