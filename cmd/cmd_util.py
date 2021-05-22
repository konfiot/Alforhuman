
import numpy as np
from src.generateColor import show_image
import sys
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
