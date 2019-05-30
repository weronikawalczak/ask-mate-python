import database_common
import data_manager
import question
import answer


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

def vote_analize(user_id, target_id, value, vote_for):
    valid_data_in_table = (check_votes(user_id, target_id, vote_for))
    # print(valid_data_in_table[0])
    if len(valid_data_in_table) == 0:
        new_vote(vote_for, target_id, user_id, value)
    else:
        vote_id = valid_data_in_table[0]['id']
        if valid_data_in_table[0]['user_vote'] > 0 and value < 0:
            change_vote(vote_id, value, target_id, vote_for)
            print('XX 1')
        elif valid_data_in_table[0]['user_vote'] < 0 and value >0:
            change_vote(vote_id, value, target_id, vote_for)
            print('XX 2')
        elif valid_data_in_table[0]['user_vote'] == 0:
            change_vote(vote_id, value, target_id, vote_for)
            print('XX 3')

def change_vote(vote_id, value, target_id, vote_for):
    if vote_for == 'q':
        question.vote_for_question(target_id, value)
        vote_counter_update(vote_id, value)
    elif vote_for == 'a':
        print('value an', value)
        answer.vote_for_answer(target_id, value)
        vote_counter_update(vote_id, value)

def new_vote(vote_for, target_id, user_id, value):
    if vote_for == 'q':
        question.vote_for_question(target_id, value)
        vote_counter_input(vote_for, target_id, user_id, value)
    elif vote_for == 'a':
        answer.vote_for_answer(target_id, value)
        vote_counter_input(vote_for, target_id, user_id, value)
        
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

