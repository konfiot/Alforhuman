import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

def generate_image_samples(num_circles: int, num_squares: int, label: int):
    # Create figure and axes
    im = np.full((200, 200, 3), 255)
    fig, ax = plt.subplots(1)

    # Display the image
    ax.imshow(im)
    for i in range(num_squares):  # Add Rectangles

        x = random.choice(range(170))
        y = random.choice(range(170))
        rect = patches.Rectangle(
            (x, y), 40, 30, linewidth=1, edgecolor='g', facecolor='none')
        ax.add_patch(rect)
        #print(x, y)
    for i in range(num_circles):  # Add Circles
        # Create a Rectangle patch
        x = random.choice(range(20, 180))
        y = random.choice(range(20, 180))
        rect = patches.Circle((x, y), 20, linewidth=1,
                              edgecolor='b', facecolor='none')
        ax.add_patch(rect)
    plt.title('label : '+str(label))
    plt.show()
    plt.close()


def assign_binary_label(num_circles, num_squares, decision_func):
    if decision_func(num_circles, num_squares) < 0:
        return 1
    else:
        return 0


def generate_dataset(dataset_size):
    # Generate 5 random numbers between 10 and 30
    circles = [random.randint(1, 5) for _ in range(dataset_size)]
    squares = [random.randint(1, 5) for _ in range(dataset_size)]

    def decision_func(x, y):
        return 2*x - y - 2
    y = []
    for i in range(dataset_size):
        y.append(assign_binary_label(circles[i], squares[i], decision_func))
    X = np.zeros((dataset_size, 2))
    X[:, 0] = circles
    X[:, 1] = squares
    y = np.array(y)

    return X, y


def show_initial_label(X, y):
    for i in range(X.shape[0]):
        generate_image_samples(
            num_circles=int(X[i, 0]), num_squares=int(X[i, 1]), label=int(y[i]))


def first_call():
    dataset_size = 20
    X, Y = generate_dataset(dataset_size=dataset_size)
    print(X)
    initial_labeled_size = 5
    labeled = [random.randint(0, dataset_size-1)
               for _ in range(initial_labeled_size)]
    show_initial_label(X[labeled], Y[labeled])


def what_do_you_think_this_is(X):
    generate_image_samples(X[:, 0], X[:, 1], label=None)
    
def AL(x, y):
    clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
    clf.fit(X, y)


first_call()

what_do_you_think_this_is()
