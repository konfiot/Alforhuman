from session_util import delete_folder_contents, generate_session_id, create_backend_session, generate_questions, store_form
from src.experiment import link_dataset_to_session, get_experiment_of_session
from src.active_learning import generate_next_query
import numpy as np
import pickle as pk
import os


def start_session():
    session_id = generate_session_id()
    create_backend_session(session_id)
    questions = generate_questions()
    return session_id, questions

def receive_form(session_id, user_form):
    store_form(session_id, user_form)


def initialize_dataset(session_id, dataset_type, al_type, dataset_path=None):
    experiment = link_dataset_to_session(
        session_id, dataset_type, al_type, dataset_path)
    experiment.store()


def get_first_images(session_id, return_raw_features=False):
    experiment = get_experiment_of_session(session_id)
    if return_raw_features:
        return [experiment.X[i, :] for i in experiment.labeled], experiment.y[experiment.labeled]
    else:
        return [experiment.images_path[i] for i in experiment.labeled], experiment.y[experiment.labeled]

def start_active_learning(session_id, return_raw_features=False):
    experiment = get_experiment_of_session(session_id)
    q = generate_next_query( experiment)
    experiment.store()
    if return_raw_features:
        return experiment.X[q, :], experiment.y[q], q
    else:
        return experiment.images_path[q], experiment.y[q], q


def store_active_learning_pred(session_id, human_label: int, q: int):
    experiment = get_experiment_of_session(session_id)
    experiment.add_human_prediction(human_label, q)
    experiment.store()

def active_learning_iteration(session_id, return_raw_features=False):
    experiment = get_experiment_of_session(session_id)
    q = generate_next_query(experiment)
    experiment.store()
    if return_raw_features:
        return experiment.X[q, :], experiment.y[q], q
    else:
        return experiment.images_path[q], experiment.y[q], q


def test_iteration(session_id, return_raw_features=False):
    experiment = get_experiment_of_session(session_id)
    test_index = experiment.test_index
    i  = experiment.test_indices[test_index]
    experiment.increment_test_index()
    experiment.store()
    if return_raw_features:
        return experiment.X[i, : ], experiment.y[i], i
    else:
        return experiment.images_path[i], experiment.y[i], i
    
    


# def test_time(session_id, return_raw_features=False):
#     experiment = get_experiment_of_session(session_id)

#     if return_raw_features:
#         return [experiment.X[i, :] for i in experiment.test_indices], experiment.y[experiment.test_indices], experiment.test_indices
#     else:
#         return [experiment.images_path[i] for i in experiment.test_indices], experiment.y[experiment.test_indices], experiment.test_indices


def store_pred(session_id, human_label_test, q):
    experiment = get_experiment_of_session(session_id)
    experiment.add_test_human_pred(human_label_test, q)
    experiment.store()



def signal_end_experiment(session_id):
    experiment = get_experiment_of_session(session_id)
    experiment.set_experiment_completed()
    experiment.store()