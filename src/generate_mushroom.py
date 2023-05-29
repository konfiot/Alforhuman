import pickle as pk
import time
import os
import random
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from scipy import misc
import pandas as pd
import numpy as np
import imageio.v2 as imageio


def show_mushroom(x, label=None):
    plt.imshow(x)
    plt.axis('off')
    if label is None:
        plt.title('What is this ?')
    else:
        plt.title('This is '+str(label))
    plt.tight_layout()
    plt.draw()
    plt.pause(2)
    plt.close()



def draw_im(x, filename):
    plt.imshow(x)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


mushroom_data_path = 'static/mushroom'


def get_mushroom_dataset():

    data_file_path = os.path.join(mushroom_data_path, 'mushroom_data.pkl')

    with open(data_file_path, "rb") as f:
        dataset_data = pk.load(f)
    X = dataset_data['X']
    images_path = []
    for i, x in enumerate(X):
        image_path = os.path.join(
            mushroom_data_path, 'mushroom_{}.png'.format(i))
        images_path.append(image_path)
    return dataset_data['X'], np.array(dataset_data['y']), images_path


def generate_and_store_mushroom_images():
    X, y, images_path = get_mushroom_dataset()
    for i, x in enumerate(X):
        draw_im(x, images_path[i])


# Generate bunch of datasets. created in data_path, create the counter file.
if __name__ == '__main__':

    if not os.path.exists(mushroom_data_path):
        print('Creating the dataset folder since it wasn\'t there\n')
        os.makedirs(mushroom_data_path)

    print('Generating mushroom')

    dataset_path = mushroom_data_path

    generate_and_store_mushroom_images()
