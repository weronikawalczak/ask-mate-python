import csv_data_handler

question_path = 'sample_data/question.csv'


def get_data():
    return csv_data_handler.read_data(question_path)


def save_question(data):
    question = {'id': 0,
                'submisson_time': 0,
                'view_number': 0,
                'vote_number': 0,
                'title': data['title'],
                'message': data['message'],
                'image': data['image']}

    return csv_data_handler.write_data(question_path, question, 'a')


def remove_question(question_id):
    data = get_data()

    for element in data:
        if element['id'] == question_id:
            data.remove(element)

    print(data)

    #return csv_data_handler.write_data(question_path, data, 'w+')


def test(question_id):
    data = get_data()

    for element in data:
        if element['id'] == question_id:
            return element
