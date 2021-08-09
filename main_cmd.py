
import random
from server_business import  *
from cmd.cmd_util import show_to_the_user, query_user
"""
This is simulating the client experience. 
A command line version of the experiment.
"""


if __name__ == "__main__":
    dataset_type = 'color'
    num_al_points = 5
    num_test_point = 5
    print('Trying out the', dataset_type, 'dataset')
   
    al_type = random.randint(0, 1) # Flip a coin to decide if we get Active Learning or Random
    
    session_id, questions = start_session()
    # Normally we ask the questions to fill the form, here we skip it and just return an empty form.
    receive_form(session_id, user_form=None)

    # Initialize dataset, either a static or dynamic dataset. After that the session id is linked to the path of the dataset.
    initialize_dataset(session_id, dataset_type, al_type)

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

        store_active_learning_pred(session_id, human_label, q)# store previous answer,
        X_query, true_y, q = active_learning_iteration(session_id, return_raw_features=True) # get next query
        human_label = query_user(X_query, true_y)
        counter += 1
        if counter == num_al_points:
            keepgoing = False

    
    counter = 0
    keepgoing = True
    while keepgoing:
        X_query, true_y, q = test_iteration(session_id,  return_raw_features=True)
        human_label_test = query_user(X_query)
        store_pred(session_id, human_label_test,q)
        counter += 1
        if counter == num_test_point:
            keepgoing = False


    signal_end_experiment(session_id)
    print('FINISHED')