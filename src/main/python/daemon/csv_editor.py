import csv
import os, sys

csv_path = "/tmp/gitup/repositories.csv"

def create_csv():
    if os.path.exists("/tmp/gitup") is False:
        os.mkdir("/tmp/gitup")
    if os.path.exists(csv_path) is True:
        return False
    header = "local_path"
    csv_file = open(csv_path, 'w+')
    writer = csv.writer(csv_file)
    writer.writerow([header])
    csv_file.close()
    return True

def add_project(path):
    if os.path.exists(csv_path) is False:
        if create_csv() is False:
            print("CSV creation failed.")
    path = os.path.normpath(path)
    csv_file = open(csv_path, 'r')
    reader = csv.reader(csv_file, delimiter=',')
    new_rows = []
    for row in reader:
        if row[0] == path:
            raise ValueError("project already exists")
        else:
            new_rows.append(row)
    new_rows.append([path])
    csv_file.close()
    csv_file = open(csv_path, 'w')
    writer = csv.writer(csv_file)
    writer.writerows(new_rows)
    csv_file.close()

def remove_project(path):
    if os.path.exists(csv_path) is False:
        raise AssertionError("No CSV exists to remove {}".format(path))
    path = os.path.normpath(path)
    csv_file = open(csv_path, 'r')
    reader = csv.reader(csv_file, delimiter=",")
    new_rows = []
    found = None
    for row in reader:
        if row[0] == path:
            found = row[0]
        else:
            new_rows.append(row)

    if found is None:
        raise ValueError("Given path {} was not already in the CSV.".format(path))
    
    csv_file.close()
    csv_file = open(csv_path, 'w')
    writer = csv.writer(csv_file)
    writer.writerows(new_rows)
    csv_file.close()