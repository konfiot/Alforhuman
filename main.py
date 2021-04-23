from server_business import *
import sys
import os
import numpy as np
import random
from generateColor import show_image
# This is basically all frontend
# Run to test locally, meant to simulate the website


def show_to_the_user(xs, y):
    for i, x in enumerate(xs):
        show_image(x, label=y[i])


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


def query_user(X_query, true_y=None):
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
    if true_y is not None:
        it_was(true_y, human_label)
    return human_label


# Simulate the client side
if __name__ == "__main__":
    dataset_type = 'color'
    # TODO ensure folder datasets is created
    dataset_path = 'dataset'
    if os.path.exists(dataset_path):
        print('creating the dataset folder since it wasn\'t there')
        os.makedirs(dataset_path)
    print('trying out the ', dataset_type, 'dataset')
    al_type = random.randint(0, 1)
    # this is first query
    session_id, questions = start_session()
    # this should be replace by some form completion, the important is to obtain the user_form
    user_form = None
    # send back the user_form to the server
    receive_form(session_id, user_form)

    # Initialize dataset, either a static or dynamic dataset but paths to images should be return
    initialize_dataset(session_id, dataset_type, dataset_path, al_type)

    X_0, y_0 = get_first_images(session_id, return_raw_features=True)
    # display first images to the user
    show_to_the_user(X_0, y_0)

    # get from server first image to display
    X_query, true_y, q = start_active_learning(
        session_id, return_raw_features=True)

    # get from the  user its classification
    human_label = query_user(X_query, true_y)

    keepgoing = True
    counter = 0
    while keepgoing:
        X_query, true_y, q = active_learning_iteration(
            session_id, human_label, q, return_raw_features=True)
        human_label = query_user(X_query, true_y)
        counter += 1
        if counter == 2:
            keepgoing = False

    # TODO test phase
    X_test, y_test = test_time(session_id, return_raw_features=True)
    score = []
    for i, x in enumerate(X_test):
        human_label = query_user(x)
        true_label = y_test[i]
        score.append(true_label == human_label)
        if i == 3:
            break
    store_results(session_id, score, al_type)
