import json


def object_to_bytes(object_to_send):
    return str.encode(json.dumps(object_to_send.__dict__))


def bytes_to_object(bytes_received):
    return json.loads(bytes_received)
