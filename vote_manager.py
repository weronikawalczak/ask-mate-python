import database_common
import data_manager
import question


@database_common.connection_handler
def check_votes(cursor, user_id, target_id, vote_for):
    cursor.execute("""SELECT * 
                                FROM votes_counter
                                WHERE user_id = %(user_id)s AND target_id = %(target_id)s AND vote_for = %(vote_for)s;""",
                   {'user_id': user_id, 'target_id':target_id, 'vote_for':vote_for})
    vote_data = cursor.fetchall()
    return vote_data

@database_common.connection_handler
def check_vote_validation(cursor, username, counter):
    cursor.execute("""SELECT * 
                                FROM votes_counter""")
    vote_data = cursor.fetchall()
    print(session['username'])
    return vote_data

def vote_analize(username, question_id, value):
    # print(username, question_id)
    user_id = data_manager.get_user_id(username)
    user_id = (user_id[0]["id"])
    valid_data_in_table = (check_votes(user_id, question_id, "q"))
    print('value', value)
    # print(vote_id)
    if len(valid_data_in_table) == 0:
        poss_vote_up = True
        poss_vote_down = True
        print('tak1')
        vote_counter_input('q', question_id, user_id, value)
    else:
        vote_id = valid_data_in_table[0]['id']
        print(valid_data_in_table)
        if valid_data_in_table[0]['user_vote'] > 0 and value < 0:
            question.vote_for_question(question_id, value)
            vote_counter_update(vote_id, -1)
            print('tak2',valid_data_in_table[0]['user_vote'])
        elif valid_data_in_table[0]['user_vote'] < 0 and value >0:
            question.vote_for_question(question_id, value)
            vote_counter_update(vote_id, 1)
            print('tak3', valid_data_in_table[0]['user_vote'])
        elif valid_data_in_table[0]['user_vote'] == 0:
            question.vote_for_question(question_id, value)
            vote_counter_update(vote_id, value)
            print('tak4', valid_data_in_table[0]['user_vote'])

    # else:
    #     print('nie')
    # print('up', poss_vote_up)
    # print('down', poss_vote_down)


@database_common.connection_handler
def vote_counter_input(cursor, vote_for, target, user_id, value):
    print('dodane do bazy')
    return cursor.execute("INSERT INTO votes_counter (vote_for, target_id, user_id, user_vote) VALUES (%s, %s, %s, %s)", (vote_for, target, user_id, value))

@database_common.connection_handler
def vote_counter_update(cursor, id, value):
    print('aktualizacja')
    return cursor.execute("""UPDATE votes_counter 
                                SET user_vote = user_vote + %(value)s
                                WHERE id = %(id)s;""", {'id': id, 'value': value})