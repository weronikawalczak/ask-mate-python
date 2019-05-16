import database_common

@database_common.connection_handler
def get_all(cursor):
    cursor.execute("""
                    SELECT * FROM question ORDER BY submission_time DESC;
                   """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def add_new_question(cursor, title, message, image):
    cursor.execute("INSERT INTO question (title, message, image) VALUES (%s, %s, %s)", (title, message, image))
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

#ANSWERS
@database_common.connection_handler
def get_answers_by_question_id(cursor, id):
    cursor.execute("""SELECT * FROM answer WHERE question_id = %(id)s;""", {'id': id})
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def add_answer(cursor, question_id, message, image):
    return cursor.execute("INSERT INTO answer (question_id, message, image) VALUES (%s, %s, %s)", (question_id, message, image))


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
def get_question_id(cursor, id):
    cursor.execute("""SELECT question_id FROM answer WHERE id = %(id)s;""", {'id': id})
    question_id = cursor.fetchone()['question_id']
    return question_id


@database_common.connection_handler
def remove_answer(cursor, id):
    return cursor.execute("""DELETE FROM answer WHERE id = %(id)s;""", {'id': id})


@database_common.connection_handler
def search_stuff(cursor, search_term):
    cursor.execute("""SELECT * FROM question WHERE message LIKE %s""", (,))
    result = cursor.fetchall()
    return result
