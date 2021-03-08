import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random


def show_image(x, label=None):
    generate_circle_square_image_samples(x[0], x[1])
    if label is None:
        plt.title('What is this ?')
    else:
        plt.title('This is '+str(label))
    plt.show()
    plt.close()


def generate_circle_square_image_samples(num_circles, num_squares):
    num_circles = int(num_circles)
    num_squares = int(num_squares)
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


def assign_binary_label(num_circles, num_squares, decision_func):
    if decision_func(num_circles, num_squares) < 0:
        return 1
    else:
        return 0


def generate_circle_square_dataset(dataset_size):
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
