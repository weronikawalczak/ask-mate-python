import data_manager


def get_data():
    return data_manager.get_all()


def get_question(question_id):
    return data_manager.get_question_by_id(question_id)


def save_question(title, message, image):
    return data_manager.add_new_question(0, 0, title, message, image)


def remove_question(id):
    return  data_manager.remove_by_id(id)



# def remove_question(question_id):
#     data = get_data()
#
#     for element in data:
#         if element['id'] == question_id:
#             data.remove(element)
#
#     print(data)
#
#     #return csv_data_handler.write_data(question_path, data, 'w+')
#
#
# def test(question_id):
#     data = get_data()
#
#     for element in data:
#         if element['id'] == question_id:
#             return element
