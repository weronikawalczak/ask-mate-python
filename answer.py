import data_manager


def get_question_answers(question_id):
    return data_manager.get_answers_by_question_id(question_id)


def add_answer(question_id, message, image):
    return data_manager.add_answer(question_id, message, image)