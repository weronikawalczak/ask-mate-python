import data_manager

def register_user(username, password, repeated_password):
    #czy sie zgadza repeated z pass
    if password != repeated_password:
        raise Exception('Passwords don\'t match')

    #check if not in db already

    #salt password

    return data_manager.register_user(username, password)