from Registration import Register
import os
import csv


class Database:
    DATABASE_PATH = "ClientDatabase.csv"

    def __init__(self):
        self.registered_clients = []
        self.open_database()

    def open_database(self):
        with open(self.DATABASE_PATH, "a+") as database:
            csv_reader = csv.reader(database)

            for row in csv_reader:
                client = Register(row[0], row[1], row[2], row[3])
                self.registered_clients.append(client)

    def register_client(self, client):
        with open(self.DATABASE_PATH, "a") as database:
            csv_writer = csv.writer(database)
            csv_writer.writerow(client.to_csv_row())

        self.registered_clients.append(client)

    def de_register_client(self, client):
        clients = []
        with open(self.DATABASE_PATH, "r") as database:
            csv_reader = csv.reader(database)
            for row in csv_reader:
                if row[0] != str(client.rq):
                    print("Adding row " + str(row))
                    clients.append(row)

        with open(self.DATABASE_PATH, "w") as database:
            csv_writer = csv.writer(database)
            csv_writer.writerows(clients)

        self.registered_clients.remove(client)

    def delete_database(self):
        if os.path.exists(self.DATABASE_PATH):
            os.remove(self.DATABASE_PATH)

        self.registered_clients.clear()
