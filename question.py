import data_manager


def get_data():
    return data_manager.get_all()


def get_first():
    return data_manager.get_first_five()


def get_question(question_id):
    return data_manager.get_question_by_id(question_id)


def save_question(title, message, image):
    return data_manager.add_new_question(title, message, image)


def remove_question(id):
    return data_manager.remove_by_id(id)


def update_question(id, title, message, image):
    return data_manager.update_question(id, title, message, image)


def add_comment(question_id, message):
    return data_manager.add_comment(question_id, message)


def get_comments(question_id):
    return data_manager.get_comments(question_id)