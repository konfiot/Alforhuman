from generateTask import generate_circle_square_dataset
import random
import pickle as pk
import os

class Dataset:
    def __init__(self, session_id, X, y, labeled_size, labeled, unlabeled, human_pred=[], q=None):
        self.session_id = session_id
        self.X = X
        self.y = y
        self.labeled_size = labeled_size
        self.labeled = labeled
        self.unlabeled = unlabeled
        self.q = None
        self.human_pred = human_pred
        print('labeled:', self.labeled)
        print('unlabeled:', self.unlabeled)

    def update_labeled_set(self, q):
        self.q
        assert q in self.unlabeled
        print('adding label', q)
        self.labeled_size += 1
        self.unlabeled.remove(q)
        self.labeled.append(q)
        print('labeled:', self.labeled)
        print('unlabeled:', self.unlabeled)

    def add_human_prediction(self, human_pred, q):
        self.human_pred.append((q, human_pred))

    def store(self):
        dataset_dict = {'X': self.X, 'y': self.y, 'labeled_size': self.labeled_size,
                        'labeled': self.labeled, 'unlabeled': self.unlabeled, 'human_pred': self.human_pred, 'q': self.q}
        file_path = get_dataset_file_path(self.session_id)
        with open(file_path, "wb") as f:
            pk.dump(dataset_dict, f)


def generate_initial_dataset(session_id):
    dataset_size = 20
    X, y = generate_circle_square_dataset(
        dataset_size=dataset_size)
    labeled_size = 2
    labeled = [random.randint(0, dataset_size-1)
               for _ in range(labeled_size)]
    unlabeled = [i for i in range(
        dataset_size) if i not in labeled]
    dataset = Dataset(session_id=session_id, X=X, y=y,
                      labeled_size=labeled_size, labeled=labeled, unlabeled=unlabeled)
    return dataset


def get_dataset_file_path(session_id):
    path = os.path.join('session', str(session_id))
    return os.path.join(path,'dataset.pkl')


def get_dataset_of_session(session_id):
    file_path = get_dataset_file_path(session_id)
    with open(file_path, "rb") as f:
        dataset_dict = pk.load(f)

    dataset = Dataset(session_id=session_id, X=dataset_dict['X'], y=dataset_dict['y'],
                      labeled_size=dataset_dict['labeled_size'], labeled=dataset_dict['labeled'], unlabeled=dataset_dict['unlabeled'], human_pred=dataset_dict['human_pred'], q=dataset_dict['q'])
    return dataset
