import database_common


@database_common.connection_handler
def get_all(cursor):
    cursor.execute("""
                    SELECT * FROM questions ORDER BY submission_time DESC;
                   """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def add_new_question(cursor, view_number, vote_number, title, message, image):
    cursor.execute("INSERT INTO questions (view_number, vote_number, title, message, image) VALUES (%s, %s, %s, %s, %s)", (view_number, vote_number, title, message, image))
    cursor.execute('SELECT LASTVAL()')  # Some psycopg2 magic to get the latest inserted id
    latest_added_question_id = cursor.fetchone()['lastval']
    return latest_added_question_id


@database_common.connection_handler
def get_question_by_id(cursor, id):
    cursor.execute("""SELECT * FROM questions WHERE id = %(id)s;""", {'id': id})
    question = cursor.fetchall()[0]
    return question


@database_common.connection_handler
def remove_by_id(cursor, id):
    return cursor.execute("""DELETE FROM questions WHERE id = %(id)s;""", {'id': id})

#ANSWERS
@database_common.connection_handler
def get_answers_by_question_id(cursor, id):
    cursor.execute("""SELECT * FROM answers WHERE question_id = %(id)s;""", {'id': id})
    answers = cursor.fetchall()
    return answers