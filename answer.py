import data_manager


def get_question_answers(question_id):
    return data_manager.get_answers_by_question_id(question_id)


def add_answer(question_id, message, image, user_id):
    return data_manager.add_answer(question_id, message, image, user_id)


def get_answer(answer_id):
    return data_manager.get_answer_by_id(answer_id)


def update_answer(answer_id, message):
    return data_manager.update_answer(answer_id, message)


def get_question_id(answer_id):
    return data_manager.get_question_id_by_answer_id(answer_id)


def remove_answer(answer_id):
    return data_manager.remove_answer(answer_id)


def vote_for_answer(answer_id, value):
    return data_manager.vote_for_answer(answer_id, value)


def add_comment(answer_id, message, user_id):
    return data_manager.add_comment_answer(answer_id, message, user_id)


def get_answers_comments(answers):
    answers_comments = {}
    for answer in answers:
        answers_comments[answer['id']] = data_manager.get_answer_comments(answer['id'])
    return answers_comments
