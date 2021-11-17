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
                    client_list.append(client)

        return client_list

    def register_client(self, client):
        with open(self.DATABASE_PATH, mode="a") as database:
            csv_writer = csv.writer(database)
            csv_writer.writerow(client.to_csv_row())

    def de_register_client(self, name):
        with open(self.DATABASE_PATH, mode="r") as database:
            csv_reader = csv.reader(database)
            clients = [row for row in csv_reader if row[0] != name]

        with open(self.DATABASE_PATH, mode="w") as database:
            csv_writer = csv.writer(database)
            csv_writer.writerows(clients)

    def delete_database(self):
        if os.path.exists(self.DATABASE_PATH):
            os.remove(self.DATABASE_PATH)
