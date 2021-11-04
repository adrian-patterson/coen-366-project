
import csv

with open("ClientDatabase.csv", mode = "r") as file:
    csvFile = csv.reader(file)

    for lines in csvFile:
        print(lines)