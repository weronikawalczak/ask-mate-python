import database_common


@database_common.connection_handler
def get_all(cursor):
    cursor.execute("""
                    SELECT * FROM question ORDER BY submission_time DESC;
                   """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_latest(cursor):
    cursor.execute("""
                    SELECT * FROM question ORDER BY submission_time DESC LIMIT 5;
                   """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def add_new_question(cursor, title, message, image, user_id):
    cursor.execute("INSERT INTO question (title, message, image, user_id) VALUES (%s, %s, %s, %s)", (title, message, image, user_id))
    cursor.execute('SELECT LASTVAL()')  # Some psycopg2 magic to get the latest inserted id
    latest_added_question_id = cursor.fetchone()['lastval']
    return latest_added_question_id


@database_common.connection_handler
def get_question_by_id(cursor, id):
    cursor.execute("""SELECT * FROM question WHERE id = %(id)s;""", {'id': id})
    question = cursor.fetchone()
    return question


@database_common.connection_handler
def remove_by_id(cursor, id):
    return cursor.execute("""DELETE FROM question WHERE id = %(id)s;""", {'id': id})


@database_common.connection_handler
def update_question(cursor, id, title, message, image):
    return cursor.execute("""UPDATE question 
                                SET title = %(title)s,
                                    message = %(message)s,
                                    image = %(image)s
                                WHERE id = %(id)s;""", {'id': id, 'title': title, 'message': message, 'image': image})


@database_common.connection_handler
def add_comment(cursor, question_id, message, user_id):
    return cursor.execute("INSERT INTO comment (question_id, message, user_id) VALUES (%s, %s, %s)", (question_id, message, user_id))


@database_common.connection_handler
def get_comments(cursor, question_id):
    cursor.execute("""SELECT * FROM comment WHERE question_id = %(question_id)s;""", {'question_id': question_id})
    comment = cursor.fetchall()
    return comment


#ANSWERS
@database_common.connection_handler
def get_answers_by_question_id(cursor, id):
    cursor.execute("""SELECT * FROM answer WHERE question_id = %(id)s ORDER BY vote_number DESC;""", {'id': id})
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def add_answer(cursor, question_id, message, image, user_id):
    return cursor.execute("INSERT INTO answer (question_id, message, image, user_id) VALUES (%s, %s, %s, %s)", (question_id, message, image, user_id))


@database_common.connection_handler
def get_answer_by_id(cursor, id):
    cursor.execute("""SELECT * FROM answer WHERE id = %(id)s;""", {'id': id})
    answer = cursor.fetchone()
    return answer


@database_common.connection_handler
def update_answer(cursor, id, message):
    return cursor.execute("""UPDATE answer 
                                SET message = %(message)s
                                WHERE id = %(id)s;""", {'id': id, 'message': message})


@database_common.connection_handler
def vote_for_answer(cursor, id):
    return cursor.execute("""UPDATE answer 
                                SET vote_number = vote_number + 1
                                WHERE id = %(id)s;""", {'id': id})


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, id):
    cursor.execute("""SELECT question_id FROM answer WHERE id = %(id)s;""", {'id': id})
    question_id = cursor.fetchone()['question_id']
    return question_id


@database_common.connection_handler
def remove_answer(cursor, id):
    return cursor.execute("""DELETE FROM answer WHERE id = %(id)s;""", {'id': id})


@database_common.connection_handler
def search(cursor, search_term):
    cursor.execute("""SELECT * FROM question 
                      WHERE message ILIKE """ "'%" + search_term + "%'" """ OR title ILIKE """ "'%" + search_term + "%'")
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def vote_for_question(cursor, id):
    return cursor.execute("""UPDATE question 
                                SET vote_number = vote_number + 1
                                WHERE id = %(id)s;""", {'id': id})


@database_common.connection_handler
def delete_comment(cursor, id):
    return cursor.execute("""DELETE FROM comment WHERE id = %(id)s;""", {'id': id})


@database_common.connection_handler
def get_question_id_by_comment_id(cursor, id):
    cursor.execute("""SELECT question_id FROM comment WHERE id = %(id)s;""", {'id': id})
    question_id = cursor.fetchone()['question_id']
    return question_id

@database_common.connection_handler
def get_answer_id_by_comment_id(cursor, id):
    cursor.execute("""SELECT answer_id FROM comment WHERE id = %(id)s;""", {'id': id})
    question_id = cursor.fetchone()['answer_id']
    return question_id


@database_common.connection_handler
def increment_view(cursor, id):
    return cursor.execute("""UPDATE question 
                                SET view_number = view_number + 1
                                WHERE id = %(id)s;""", {'id': id})


@database_common.connection_handler
def add_comment_answer(cursor, answer_id, message, username):
    return cursor.execute("INSERT INTO comment (answer_id, message, username) VALUES (%s, %s, %s)", (answer_id, message, username))


@database_common.connection_handler
def get_answer_comments(cursor, answer_id):
    cursor.execute("""SELECT * FROM comment WHERE answer_id = %(answer_id)s;""", {'answer_id': answer_id})
    comment = cursor.fetchall()
    return comment

#USER


@database_common.connection_handler
def register_user(cursor, username, password):
    cursor.execute("INSERT INTO person (username, password) VALUES (%s, %s)", (username, password))
    person = cursor.fetchall()
    return person


@database_common.connection_handler
def get_user(cursor, username):
    cursor.execute("SELECT * FROM person WHERE username = %(username)s ", {'username': username})
    person = cursor.fetchone()
    return person


@database_common.connection_handler
def gain_reputation(cursor, username, counter):
    return cursor.execute("""UPDATE person 
                                SET reputation = reputation + int(counter)
                                WHERE username = %(username)s;""", {'username': username})


