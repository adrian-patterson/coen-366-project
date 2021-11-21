import requests
from flask import Flask, render_template, Response, request
from ClientRequests import RegisterWithServer, DeRegisterFromServer, RemoveFilesFromServer, PublishFilesToServer
from Client import Client

app = Flask("__main__", static_url_path='', static_folder='build', template_folder='build')
client = Client()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/client", methods=["GET"])
def get_client_info():
    return {
        'rq': client.rq,
        'name': client.name,
        'ipAddress': client.ip_address,
        'udpSocket': client.UDP_PORT,
        'tcpSocket': client.tcp_socket,
        'listOfAvailableFiles': client.list_of_available_files
    }


@app.route("/register", methods=["POST"])
def register():
    register_request = request.get_json(force=True)
    name = register_request['name']
    server_ip_address = register_request['serverIpAddress']
    client.name = name
    registration = RegisterWithServer(client, server_ip_address)
    registration.start()
    return {'register': registration.join()}


@app.route("/de_register", methods=["POST"])
def de_register():
    de_registration = DeRegisterFromServer(client)
    de_registration.start()
    de_registration.join()
    return Response(status=201)


@app.route("/publish", methods=["POST"])
def publish_files():
    publish_request = request.get_json(force=True)
    list_of_files_to_publish = publish_request["filesSelected"]
    publish = PublishFilesToServer(client, list_of_files_to_publish)
    publish.start()
    publish.join()
    return Response(status=201)


@app.route("/remove", methods=["POST"])
def remove_files():
    remove_request = request.get_json(force=True)
    list_of_files_to_remove = remove_request["filesSelected"]
    remove = RemoveFilesFromServer(client, list_of_files_to_remove)
    remove.start()
    remove.join()
    return Response(status=201)


@app.route("/shutdown", methods=['GET'])
def shutdown():
    shutdown_func = requests.request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down..."


def start():
    app.run(host='', threaded=True, port=5000, debug=True)


def stop():
    resp = requests.get('http://localhost:5002/shutdown')


start()
stop()
