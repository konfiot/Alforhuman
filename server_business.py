from session_util import delete_folder_contents, generate_session_id, create_backend_session, generate_questions, store_form
from src.experiment import link_dataset_to_session, get_experiment_of_session
from src.active_learning import generate_next_query
import numpy as np
import pickle as pk
import os
# Server Business 1


def start_session():
    session_id = generate_session_id()
    create_backend_session(session_id)
    questions = generate_questions()
    return session_id, questions


# Server Business 2
def receive_form(session_id, user_form):
    store_form(session_id, user_form)


def initialize_dataset(session_id, dataset_type, dataset_path, al_type):
    experiment = link_dataset_to_session(
        session_id, dataset_type, dataset_path, al_type)
    experiment.store()


def get_first_images(session_id, return_raw_features=False):
    experiment = get_experiment_of_session(session_id)
    if return_raw_features:
        return [experiment.X[i, :] for i in experiment.labeled], experiment.y[experiment.labeled]
    else:
        return [experiment.images_path[i] for i in experiment.labeled], experiment.y[experiment.labeled]
# Server Business 3


def start_active_learning(session_id, return_raw_features=False):
    experiment = get_experiment_of_session(session_id)
    q = generate_next_query( experiment)
    experiment.store()
    if return_raw_features:
        return experiment.X[q, :], experiment.y[q], q
    else:
        return experiment.images_path[q], experiment.y[q], q

# Server Business 4


def active_learning_iteration(session_id, human_label: int, q: int, return_raw_features=False):
    experiment = get_experiment_of_session(session_id)
    experiment.add_human_prediction(human_label, q)
    q = generate_next_query(experiment)
    experiment.store()
    if return_raw_features:
        return experiment.X[q, :], experiment.y[q], q
    else:
        return experiment.images_path[q], experiment.y[q], q

# Server Business 5


def test_time(session_id, return_raw_features=False):
    experiment = get_experiment_of_session(session_id)

    if return_raw_features:
        return [experiment.X[i, :] for i in experiment.test_indices], experiment.y[experiment.test_indices]
    else:
        return [experiment.images_path[i] for i in experiment.test_indices], experiment.y[experiment.test_indices]

# Server Business 6


def store_score(session_id, score):
    experiment = get_experiment_of_session(session_id)
    experiment.set_score(score)
    experiment.store()

