import json
from datetime import datetime


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
