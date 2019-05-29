import data_manager


def get_data():
    return data_manager.get_all()


def get_latest():
    return data_manager.get_latest()


def get_question(question_id):
    return data_manager.get_question_by_id(question_id)


def save_question(title, message, image, username):
    return data_manager.add_new_question(title, message, image, username)


def remove_question(id):
    return data_manager.remove_by_id(id)


def update_question(id, title, message, image):
    return data_manager.update_question(id, title, message, image)


def add_comment(question_id, message, username):
    return data_manager.add_comment(question_id, message, username)


def get_comments(question_id):
    return data_manager.get_comments(question_id)


def vote_for_question(question_id):
    return data_manager.vote_for_question(question_id)


def delete_comment(comment_id):
    return data_manager.delete_comment(comment_id)


def get_question_by_comment_id(comment_id):
    question_id = data_manager.get_question_id_by_comment_id(comment_id)
    if question_id is None:
        answer_id = data_manager.get_answer_id_by_comment_id(comment_id)
        question_id = data_manager.get_question_id_by_answer_id(answer_id)
    return question_id


def increment_view(id):
    return data_manager.increment_view(id)