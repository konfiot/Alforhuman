from session_util import delete_folder_contents, generate_session_id, create_backend_session, generate_questions, store_form
from src.experiment import link_dataset_to_session, get_experiment_of_session
from src.active_learning import generate_next_query
import numpy as np
import pickle as pk
import os


class ServerBusiness():
    def __init__(self, db):
        self.db = db

    def start_session(self):
        session_id = generate_session_id()
        create_backend_session(session_id)
        questions = generate_questions()
        return session_id, questions

    def receive_form(self, session_id, user_form):
        store_form(session_id, user_form)

    def initialize_dataset(self, session_id, dataset_type, al_type, dataset_path=None):
        experiment = link_dataset_to_session(
            session_id, dataset_type, al_type, dataset_path, db=self.db)
        experiment.store(db=self.db)

    def get_first_images(self, session_id, return_raw_features=False):
        experiment = get_experiment_of_session(session_id, db=self.db)
        if return_raw_features:
            return [experiment.X[i, :] for i in experiment.labeled], experiment.y[experiment.labeled]
        else:
            return [experiment.images_path[i] for i in experiment.labeled], experiment.y[experiment.labeled]

    def start_active_learning(self, session_id, return_raw_features=False):
        experiment = get_experiment_of_session(session_id, db=self.db)
        q = generate_next_query(experiment)
        experiment.store(db=self.db)
        if return_raw_features:
            return experiment.X[q, :], experiment.y[q], q
        else:
            return experiment.images_path[q], experiment.y[q], q

    def store_active_learning_pred(self, session_id, human_label: int, q: int):
        experiment = get_experiment_of_session(session_id, db=self.db)
        experiment.add_human_prediction(human_label, q)
        experiment.store(db=self.db)

    def active_learning_iteration(self, session_id, return_raw_features=False):
        experiment = get_experiment_of_session(session_id, db=self.db)
        q = generate_next_query(experiment)
        experiment.store(db=self.db)
        if return_raw_features:
            return experiment.X[q, :], experiment.y[q], q
        else:
            return experiment.images_path[q], experiment.y[q], q

    def test_iteration(self, session_id, return_raw_features=False):
        experiment = get_experiment_of_session(session_id, db=self.db)
        test_index = experiment.test_index
        i = experiment.test_indices[test_index]
        experiment.increment_test_index()
        experiment.store(db=self.db)
        if return_raw_features:
            return experiment.X[i, :], experiment.y[i], i
        else:
            return experiment.images_path[i], experiment.y[i], i

    def store_pred(self, session_id, human_label_test, q):
        experiment = get_experiment_of_session(session_id, db=self.db)
        experiment.add_test_human_pred(human_label_test, q)
        experiment.store(db=self.db)

    def signal_end_experiment(self, session_id):
        experiment = get_experiment_of_session(session_id, db=self.db)
        experiment.set_experiment_completed()
        experiment.store(db=self.db)
