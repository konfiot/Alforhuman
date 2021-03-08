from server_business import *
from generateTask import show_image
import sys

# This is basically all frontend


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


def query_user(X_query, true_y):
    human_label = what_is_this_bb(X_query)

    for answer in sys.stdin:
        answer = answer.replace('\n', '')
        if answer == '0':
            human_label = 0
            break
        elif answer == '1':
            human_label = 1
            break
        else:
            print('input 0 or 1 plz')
    it_was(true_y, human_label)
    return human_label


# Simulate the client side
if __name__ == "__main__":
    # this is first query
    session_id, questions = start_session()
    # this should be replace by some form completion, the important is to obtain the user_form
    user_form = build_user_form(questions)
    # send back the user_form to the server
    X_0, y_0 = receive_form(session_id, user_form)
    # display first images to the user
    show_to_the_user(X_0, y_0)
    # get from server first image to display
    X_query, true_y, q = start_active_learning(session_id)
    # get from the  user its classification
    human_label = query_user(X_query, true_y)

    keepgoing = True
    counter = 0
    while keepgoing:
        X_query, true_y, q = active_learning_iteration(
            session_id, human_label, q)
        human_label = query_user(X_query, true_y)
        counter += 1
        if counter == 5:
            keepgoing = False
    print("that's it thanks you")
    # TODO test phase
    # X_test = test_time(session_id)
