from ClientData import ClientData
import os
import csv


class Database:
    DATABASE_PATH = "ClientDatabase.csv"

    def open_database(self):
        client_list = []
        if os.path.exists(self.DATABASE_PATH):
            with open(self.DATABASE_PATH, mode="r") as database:
                csv_reader = csv.reader(database)
                for row in csv_reader:
                    client = ClientData(row[1], row[2], row[3], row[4])
                    client.rq = row[0]
                    client.list_of_available_files = self.str_to_list(row[5])
                    for file_name in client.list_of_available_files:
                        print(file_name)
                    client_list.append(client)

        return client_list

    def register_client(self, client):
        with open(self.DATABASE_PATH, mode="a", newline="") as database:
            csv_writer = csv.writer(database)
            csv_writer.writerow(client.to_csv_row())

    def de_register_client(self, name):
        with open(self.DATABASE_PATH, mode="r") as database:
            csv_reader = csv.reader(database)
            clients = [row for row in csv_reader if row[1] != str(name)]

        with open(self.DATABASE_PATH, mode="w", newline="") as database:
            csv_writer = csv.writer(database)
            csv_writer.writerows(clients)

    def publish_files(self, name, files):
        clients = []
        with open(self.DATABASE_PATH, mode="r") as database:
            csv_reader = csv.reader(database)
            for row in csv_reader:
                if row[1] == name:
                    clientUpdate = ClientData(row[1],row[2],row[3],row[4])
                    clientUpdate.rq = row[0]
                    clientUpdate.list_of_available_files = files
                    clients.append(clientUpdate.to_csv_row())
                else:
                    clients.append(row)

        with open(self.DATABASE_PATH, mode="w", newline="") as database:
            csv_writer = csv.writer(database)
            csv_writer.writerows(clients)

    def delete_database(self):
        if os.path.exists(self.DATABASE_PATH):
            os.remove(self.DATABASE_PATH)

    def str_to_list(self, list_as_str):
    
        list_as_list = []
        for element in list_as_str.replace("]","").replace("[","").replace("'","").replace('"','').split(","):
            list_as_list.append(element.strip())
        return list_as_list
