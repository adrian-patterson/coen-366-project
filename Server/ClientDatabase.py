import json
from ClientData import ClientData
import os


class Database:

    DATABASE_PATH = "ClientDatabase.csv"

    def open_database(self):
        client_list = []
        if os.path.exists(self.DATABASE_PATH):
            with open(self.DATABASE_PATH, mode="r") as database:
                for client_json in database.readlines():
                    client = ClientData(**json.loads(client_json))
                    client_list.append(client)

        return client_list

    def add_client(self, client):
        with open(self.DATABASE_PATH, mode="a", newline="") as database:
            database.write(json.dumps(client.__dict__) + "\n")

    def remove_client(self, name):
        clients = []
        new_clients_list = []

        with open(self.DATABASE_PATH, mode="r") as database:
            clients = (client.rstrip() for client in database)
            clients = (client for client in clients if client)
            new_clients_list = [client for client in clients if json.loads(client)[
                "name"] != name]

        with open(self.DATABASE_PATH, mode="w", newline="") as database:
            for client in new_clients_list:
                database.write(client + "\n")

    # TODO: update client

    def publish_files(self, name, files):
        clients = []
        new_clients_list = []

        with open(self.DATABASE_PATH, mode="r") as database:
            clients = (client.rstrip() for client in database)
            clients = (client for client in clients if client)

            for client_json in clients:
                if client_json:
                    client = json.loads(client_json)
                    if client["name"] == name:
                        client["list_of_available_files"] = files
                        new_clients_list.append(json.dumps(client))
                    else:
                        new_clients_list.append(client_json)

        with open(self.DATABASE_PATH, mode="w", newline="") as database:
            for client in new_clients_list:
                database.write(client + "\n")

    def delete_database(self):
        if os.path.exists(self.DATABASE_PATH):
            os.remove(self.DATABASE_PATH)
