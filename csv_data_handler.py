import csv

answer_path = 'sample_data/answer.csv'

def read_data(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        content = []
        for row in reader:
            content.append(row)
    return content



