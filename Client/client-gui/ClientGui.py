import json
import requests
from flask import Flask, render_template, Response, request
from ClientRequests import *
from Client import Client

app = Flask("__main__", static_url_path='',
            static_folder='build', template_folder='build')
client = Client()
client.start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/app")
def app_page():
    client.get_list_of_available_files()
    return render_template("index.html")


@app.route("/client", methods=["GET"])
def get_client_info():
    return {
        'name': client.name,
        'ipAddress': client.ip_address,
        'udpSocket': client.udp_socket.getsockname()[1],
        'tcpSocket': client.tcp_socket.getsockname()[1],
        'listOfAvailableFiles': client.list_of_available_files
    }


@app.route("/login", methods=["POST"])
def login():
    register_request = request.get_json(force=True)
    name = register_request['name']
    server_ip_address = register_request['serverIpAddress']
    client.server_ip_address = server_ip_address
    client.server_address = (server_ip_address, client.SERVER_UDP_PORT)
    retrieve_client = RetrieveClientInfoFromServer(client, name)
    retrieve_client.start()
    result = retrieve_client.join()
    if isinstance(result, RetrieveInfoResponse):
        client.name = result.name
        client.udp_socket = client.udp_init(0)
        return {'login': True}
    else:
        return {'login': False}


@app.route("/retrieveall", methods=["GET"])
def retrieve_all():
    retrieve = RetrieveAllClientsFromServer(client)
    retrieve.start()

    result = retrieve.join()
    client_json_list = []
    if isinstance(result, list):
        for c in result:
            c_json = json.loads(c)
            if c_json["name"] != client.name:
                client_json_list.append({'name': c_json["name"], 'ipAddress': c_json["ip_address"],
                                        'tcpSocket': c_json["tcp_socket"], 'listOfAvailableFiles': c_json["list_of_available_files"]})
        return {'retrieve': client_json_list}, 200
    else:
        return {'retrieve': result}, 400


@app.route("/searchfile", methods=["POST"])
def search_file():
    search_file_request = request.get_json(force=True)
    file_name = search_file_request["fileName"]

    search_file = SearchFileFromServer(client, file_name)
    search_file.start()
    result = search_file.join()
    if not isinstance(result, str):
        return {'searchfile': result.__dict__}, 200
    else:
        return {'searchfile': result}, 400


@app.route("/retrieve", methods=["POST"])
def retrieve():
    retrieve_client_request = request.get_json(force=True)
    name = retrieve_client_request["name"]

    retrieve_client = RetrieveClientInfoFromServer(client, name)
    retrieve_client.start()

    result = retrieve_client.join()
    if not isinstance(result, str):
        return {'retrieve': result.__dict__}
    else:
        return {'retrieve': result}, 400


@app.route("/update", methods=["POST"])
def update():
    update_request = request.get_json(force=True)
    ip_address = update_request["ipAddress"]
    udp_socket = update_request["udpSocket"]
    tcp_socket = update_request["tcpSocket"]
    client.ip_address = ip_address

    update = UpdateClientContact(
        client, ip_address, udp_socket, tcp_socket)
    update.start()
    return {'update': update.join()}


@app.route("/download", methods=["POST"])
def download():
    download_request = request.get_json(force=True)
    file_name = download_request["fileName"]
    ip_address = download_request["ipAddress"]
    tcp_socket = download_request["tcpSocket"]

    download = DownloadFileFromPeer(
        client, file_name, ip_address, int(tcp_socket))
    download.start()
    return {'download': download.join()}


@ app.route("/register", methods=["POST"])
def register():
    register_request = request.get_json(force=True)
    name = register_request['name']
    server_ip_address = register_request['serverIpAddress']
    client.name = name
    registration = RegisterWithServer(client, server_ip_address)
    registration.start()
    return {'register': registration.join()}


@ app.route("/de_register", methods=["POST"])
def de_register():
    de_registration = DeRegisterFromServer(client)
    de_registration.start()
    de_registration.join()
    return Response(status=201)


@ app.route("/publish", methods=["POST"])
def publish_files():
    publish_request = request.get_json(force=True)
    list_of_files_to_publish = publish_request["filesSelected"]
    publish = PublishFilesToServer(client, list_of_files_to_publish)
    publish.start()
    return {'publish': publish.join()}


@ app.route("/remove", methods=["POST"])
def remove_files():
    remove_request = request.get_json(force=True)
    list_of_files_to_remove = remove_request["filesSelected"]
    remove = RemoveFilesFromServer(client, list_of_files_to_remove)
    remove.start()
    return {'remove': remove.join()}


@ app.route("/shutdown", methods=['GET'])
def shutdown():
    shutdown_func = requests.request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down..."


def start():
    app.run(host='', threaded=True, port=0, debug=True)


def stop():
    resp = requests.get('http://localhost:5002/shutdown')


start()
stop()
