import csv
import os

csv_path = "/tmp/gitup/repositories.csv"

def create_csv():
    if os.path.exists("/tmp/gitup") is False:
        os.mkdir("/tmp/gitup")
    if os.path.exists(csv_path) is True:
        return False
    header = "last_pulled"
    csv_file = open(csv_path, 'w+')
    writer = csv.writer(csv_file)
    writer.writerow(header)
    csv_file.close()
    return True    

def add_project(path):
    if os.path.exists(csv_path) is False:
        if create_csv() is False:
            print("CSV creation failed.")
    path = os.path.normpath(path)
    csv_file = open(csv_path, 'r')
    reader = csv.reader(csv_file)
    new_rows = []
    line = 0
    for row in reader:
        if line != 0 and row[0] == path:
            raise ValueError("project already exists")
        else:
            new_rows.append(','.join(row))
    new_rows.append(path)
    csv_file.close()
    csv_file = open(csv_path, 'w')
    writer = csv.writer(csv_file)
    writer.writerows(new_rows)
    csv_file.close()
