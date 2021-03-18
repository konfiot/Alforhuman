import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random


def show_image(x, label=None):
    A = np.zeros((100, 100, 3))

    A[:, :, :] = x/255
    plt.imshow(A)
    if label is None:
        plt.title('What is this ?')
    else:
        plt.title('This is '+str(label))
    plt.show()
    plt.close()


def assign_binary_label(color, decision_func):
    if decision_func(color) < 0:
        return 1
    else:
        return 0


def generate_dataset(dataset_size):

    color_corner_a = [0, 130, 221]
    color_corner_b = [134, 0, 13]
    # A = np.zeros((100, 100, 3))

    # A[:, :, :] = [123, 34, 83]
    # plt.imshow(A)
    # plt.show()
    reds = [random.randint(color_corner_a[0], color_corner_b[0])
            for _ in range(dataset_size)]
    blues = [random.randint(color_corner_b[1], color_corner_a[1])
             for _ in range(dataset_size)]
    greens = [random.randint(color_corner_b[2], color_corner_a[2])
              for _ in range(dataset_size)]

    def decision_func(color):
        r = np.abs(color_corner_b[0]-color_corner_a[0])
        g = np.abs(color_corner_b[1]-color_corner_a[1])
        b = np.abs(color_corner_b[2]-color_corner_a[2])
        if color[0] < r:
            return -1
        else:
            return 1

    y = []
    for i in range(dataset_size):
        color = [reds[i], blues[i], greens[i]]
        y.append(assign_binary_label(color, decision_func))
    X = np.zeros((dataset_size, 3))
    X[:, 0] = reds
    X[:, 1] = blues
    X[:, 2] = greens
    y = np.array(y)

    return X, y


if __name__ == '__main__':
    X, y = generate_dataset(50)
    
    for i in range(50):
        show_image(X[i, :], y[i])
