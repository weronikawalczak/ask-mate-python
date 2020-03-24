import csv

answer_path = 'sample_data/answer.csv'
fieldnames = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']

def read_data(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        content = []
        for row in reader:
            content.append(row)
    return content

def write_data(file_path, data, mode, fieldnames=fieldnames):
    with open(file_path, mode, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writerow(data)
