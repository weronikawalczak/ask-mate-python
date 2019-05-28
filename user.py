import data_manager
import pass_service

def register_user(username, password, repeated_password):
    #czy sie zgadza repeated z pass
    if password != repeated_password:
        raise Exception('Passwords don\'t match')

    #check if not in db already

    #salt password
    hashed_pass = pass_service.hash_password(password)

    return data_manager.register_user(username, hashed_pass)
















def gain_reputation(counter):
    user_id = "test"
    data_manager.gain_reputation(user_id, counter)

    #current user_id
    #reputation '+5'
    #insert reputation into db