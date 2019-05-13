import data_manager


def get_data():
    return data_manager.get_all()


def get_question(question_id):
    return data_manager.get_question_by_id(question_id)


def save_question(title, message, image):
    return data_manager.add_new_question(title, message, image)


def remove_question(id):
    return data_manager.remove_by_id(id)


def update_question(id, title, message, image):
    return data_manager.update_question(id, title, message, image)