
import random
from server_business import  get_first_images, start_active_learning, initialize_dataset, store_score, start_session, test_time, receive_form, active_learning_iteration
from cmd.cmd_util import show_to_the_user, query_user
"""
This is simulating the client experience. 
A command line version of the experiment.
"""


if __name__ == "__main__":
    dataset_type = 'color'
    data_path = 'data'
    num_al_points = 5
    num_test_point = 3
    print('Trying out the', dataset_type, 'dataset')
    # Flip a coin to decide if we get Active Learning or Random
    al_type = random.randint(0, 1)
    session_id, questions = start_session()
    # Normally we ask the questions to fill the form, here we skip it and just return an empty form.
    receive_form(session_id, user_form=None)

    # Initialize dataset, either a static or dynamic dataset. After that the session id is linked to the path of the dataset.
    initialize_dataset(session_id, dataset_type, data_path, al_type)

    # get raw features (vector) of x, not the path to the images.
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
        if counter == num_al_points:
            keepgoing = False

    X_test, y_test = test_time(session_id, return_raw_features=True)
    score = []
    for i, x in enumerate(X_test):
        human_label = query_user(x)
        true_label = y_test[i]
        score.append(true_label == human_label)
        if i == num_test_point:  # stop after 3 for test
            break

    store_score(session_id, score)
