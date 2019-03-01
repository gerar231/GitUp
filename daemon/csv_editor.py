import csv
import os

@staticmethod
def add_project(csv_file, path):
    path = os.path.normpath(path);
    csv = open(csv_file, 'r')
    reader = csv.reader(csv)
    new_rows = []
    line = 0
    for row in reader:
        if line != 0 && row[0].equals(path):
            raise Error("project already exists")
        else:
            new_rows.append(','.join(row))
    new_rows.append(path)
    csv.close()
    csv = open(csv_file, 'w')
    writer = csv.writer(csv)
    writer.writerows(newrows)

@staticmethod
def create_csv(csv_file)
    header = "last_pulled"
    csv = open(csv_file, 'w+')
    writer = csv.writer(csv)
    writer.writerow(header)


