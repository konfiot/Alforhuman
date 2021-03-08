from server_business import *
from generateTask import show_image
import sys


def show_to_the_user(X_0, y_0):
    for i, x in enumerate(X_0):
        show_image(x, label=y_0[i])


def what_is_this_bb(X_query):
    show_image(X_query)


def it_was(true_y, human_label):
    if true_y == human_label:
        print('Yeah it was', str(true_y), ', you got it bb!')
    else:
        print('Nope it was', str(true_y), 'you suck.')


def build_user_form(questions):
    print(questions)
    user_form = []
    for answer in sys.stdin:
        user_form.append(answer)
        break
    return user_form


if __name__ == "__main__":

    session_id, questions = start_session()
    user_form = build_user_form(questions)
    X_0, y_0 = receive_form(session_id, user_form)
    
    show_to_the_user(X_0, y_0)

    X_query, true_y = start_active_learning(session_id)
    human_label = what_is_this_bb(X_query)
    it_was(true_y)

    keepgoing = True
    while keepgoing:
        X_query, true_y = active_learning_iteration(session_id, human_label, q)
        human_label = what_is_this_bb(X_query)
        it_was(true_y, human_label)

    X_test = test_time(session_id)
