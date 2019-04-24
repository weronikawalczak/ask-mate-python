import  csv_data_handler

question_path = '/home/franek/ask-mate-python/sample_data/question.csv'


def get_data():
    return csv_data_handler.read_data(question_path)

