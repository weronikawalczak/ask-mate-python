import data_manager


def get_question_answers(question_id):
    return data_manager.get_answers_by_question_id(question_id)


def add_answer(question_id, message, image):
    return data_manager.add_answer(question_id, message, image)


def get_answer(answer_id):
    return data_manager.get_answer_by_id(answer_id)


def update_answer(answer_id, message):
    return data_manager.update_answer(answer_id, message)


def get_question_id(answer_id):
    return data_manager.get_question_id(answer_id)


def remove_answer(answer_id):
    return data_manager.remove_answer(answer_id)


def vote_for_answer(answer_id):
    return data_manager.vote_for_answer(answer_id)
