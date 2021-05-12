
import sys
import os
import random
from cmd.cmd_util import *
"""
This is simulating the client experience. 
A command line version of the experiment.
"""


if __name__ == "__main__":
    dataset_type = 'color'
    data_path = 'data'
    number_of_queries = 2

    if not os.path.exists(data_path):
        print('Creating the dataset folder since it wasn\'t there\n')
        os.makedirs(data_path)
   
    print('Trying out the', dataset_type, 'dataset')
    al_type = random.randint(0, 1) # Flip a coin to decide if we get Active Learning or Random 
    
    session_id, questions = start_session() 
    # Normally we ask the questions to fill the form, here we skip it and just return an empty form.
    receive_form(session_id, user_form=None) 

    # Initialize dataset, either a static or dynamic dataset. After that the session id is linked to the path of the dataset.
    initialize_dataset(session_id, dataset_type, data_path, al_type)

    X_0, y_0 = get_first_images(session_id, return_raw_features=True) # get raw features (vector) of x, not the path to the images.
    
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
        if counter == number_of_queries:
            keepgoing = False

    
    X_test, y_test = test_time(session_id, return_raw_features=True)
    score = []
    for i, x in enumerate(X_test):
        human_label = query_user(x)
        true_label = y_test[i]
        score.append(true_label == human_label)
        if i == 3: # stop after 3 for test
            break
    
    store_score(session_id, score)
    