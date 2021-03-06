import database_common

#QUESTIONS
@database_common.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT question.*, person.username FROM question 
                    JOIN person ON question.user_id = person.id 
                    ORDER BY question.submission_time DESC;
                   """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_latest_questions(cursor):
    cursor.execute("""
                    SELECT question.*, person.username FROM question 
                    JOIN person ON question.user_id = person.id 
                    ORDER BY question.submission_time DESC
                    LIMIT 5;
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
    cursor.execute("""
                    SELECT question.*, person.username FROM question 
                    JOIN person ON question.user_id = person.id 
                    WHERE question.id = %(id)s;""", {'id': id})
    question = cursor.fetchone()
    return question


@database_common.connection_handler
def remove_question_by_id(cursor, id, session_user_id):
    return cursor.execute("""DELETE FROM question WHERE id = %(id)s AND user_id = %(session_user_id)s;""", {'id': id, 'session_user_id': session_user_id})


@database_common.connection_handler
def update_question(cursor, id, title, message, image):
    return cursor.execute("""UPDATE question 
                                SET title = %(title)s,
                                    message = %(message)s,
                                    image = %(image)s
                                WHERE id = %(id)s;""", {'id': id, 'title': title, 'message': message, 'image': image})


@database_common.connection_handler
def add_comment_to_question(cursor, question_id, message, user_id):
    return cursor.execute("INSERT INTO comment (question_id, message, user_id) VALUES (%s, %s, %s)", (question_id, message, user_id))


@database_common.connection_handler
def vote_for_question(cursor, id):
    return cursor.execute("""UPDATE question 
                                SET vote_number = vote_number + 1
                                WHERE id = %(id)s;""", {'id': id})


@database_common.connection_handler
def increment_question_views(cursor, id):
    return cursor.execute("""UPDATE question 
                                SET view_number = view_number + 1
                                WHERE id = %(id)s;""", {'id': id})


#ANSWERS
@database_common.connection_handler
def get_answers_by_question_id(cursor, id):
    cursor.execute("""
                    SELECT answer.*, person.username FROM answer 
                    JOIN person ON answer.user_id = person.id 
                    WHERE question_id = %(id)s 
                    ORDER BY vote_number DESC;""", {'id': id})
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
def vote_for_answer(cursor, id, value):
    return cursor.execute("""UPDATE answer 
                                SET vote_number = vote_number + %(value)s
                                WHERE id = %(id)s;""", {'id': id, 'value': value})


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
    cursor.execute("""
                    SELECT question.*, person.username FROM question 
                    JOIN person ON question.user_id = person.id 
                    WHERE message ILIKE """ "'%" + search_term + "%'" """ OR title ILIKE """ "'%" + search_term + "%'")
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def vote_for_question(cursor, id, value):
    return cursor.execute("""UPDATE question 
                                SET vote_number = vote_number + %(value)s
                                WHERE id = %(id)s;""", {'id': id, 'value': value})


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
def add_comment_answer(cursor, answer_id, message, user_id):
    return cursor.execute("INSERT INTO comment (answer_id, message, user_id) VALUES (%s, %s, %s)", (answer_id, message, user_id))


@database_common.connection_handler
def get_question_comments(cursor, question_id):
    cursor.execute("""
                    SELECT comment.*, person.username FROM comment 
                    JOIN person ON comment.user_id = person.id 
                    WHERE question_id = %(question_id)s;""", {'question_id': question_id})
    comment = cursor.fetchall()
    return comment


@database_common.connection_handler
def get_answer_comments(cursor, answer_id):
    cursor.execute("""
                    SELECT comment.*, person.username FROM comment 
                    JOIN person ON comment.user_id = person.id 
                    WHERE answer_id = %(answer_id)s;""", {'answer_id': answer_id})
    comment = cursor.fetchall()
    return comment


#USER
@database_common.connection_handler
def register_user(cursor, username, password):
    return cursor.execute("INSERT INTO person (username, password) VALUES (%s, %s)", (username, password))


@database_common.connection_handler
def list_users(cursor):
    cursor.execute("SELECT "
                   # "CAST (id AS VARCHAR),"
                   "username AS User,"
                   # "password,"
                   "LEFT (CAST (registration_date as VARCHAR),10) AS registration_date,"
                   "CAST (reputation as VARCHAR) "
                   "FROM person "
                   "ORDER BY username")

    users = cursor.fetchall()
    return users


@database_common.connection_handler
def get_user(cursor, username):
    cursor.execute("SELECT * FROM person WHERE username = %(username)s ", {'username': username})
    user = cursor.fetchone()
    return user


@database_common.connection_handler
def gain_reputation(cursor, username, counter):
    return cursor.execute("""UPDATE person 
                                SET reputation = reputation + int(counter)
                                WHERE username = %(username)s;""", {'username': username})


@database_common.connection_handler
def get_user_id(cursor, username):
    cursor.execute("SELECT id FROM person WHERE username = %(username)s", {'username': username})
    user_id = cursor.fetchall()
    return user_id


@database_common.connection_handler
def get_questions_by_user_id(cursor, user_id):
    cursor.execute("SELECT question.*, person.username FROM question join person on question.user_id = person.id WHERE person.id = %(user_id)s;", {'user_id': user_id})
    title = cursor.fetchall()
    return title


@database_common.connection_handler
def get_answer_by_user_id(cursor, user_id):
    cursor.execute("SELECT * FROM answer join person on answer.user_id = person.id WHERE person.id = %(user_id)s;", {'user_id': user_id})
    title = cursor.fetchall()
    return title


@database_common.connection_handler
def get_comments_by_user_id(cursor, user_id):
    cursor.execute("SELECT comment.*, answer.question_id as answer_question_id FROM comment join person on comment.user_id = person.id full outer join answer on comment.answer_id = answer.id WHERE person.id = %(user_id)s;", {'user_id': user_id})
    title = cursor.fetchall()
    return title


