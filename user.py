from flask import session, redirect
import data_manager
import pass_service


def register_user(username, password, repeated_password):
    #czy sie zgadza repeated z pass
    if password != repeated_password:
        raise Exception('Passwords don\'t match')

    #check if pass is empty
    if password == "":
        raise Exception('Password cannot be empty')

    if username == "":
        raise Exception('Username cannot be empty')

    #salt password
    hashed_pass = pass_service.hash_password(password)

    return data_manager.register_user(username, hashed_pass)


def login_user(username, password):
    if username == "" or password == "":
        return False

    user_data = data_manager.get_user(username)
    if user_data:
        if pass_service.verify_password(password, user_data['password']):
            return user_data
    else:
        return False


def gain_reputation(username, counter):
    data_manager.gain_reputation(username, counter)


def logged_in(function):
    def wrapper():
        if session:
            return function()
        else:
            return redirect('/')
    return wrapper


def get_questions_by_user_id(user_id):
    return data_manager.get_questions_by_user_id(user_id)


def get_answers_by_user_id(user_id):
    return data_manager.get_answer_by_user_id(user_id)


def get_comments_by_user_id(user_id):
    return data_manager.get_comments_by_user_id(user_id)
