import pandas as pd
import tensorflow as tf
from matrix import Matrix
import numpy as np


def prep_load_data():
    pass


def load_data(train_split=0.7, remove_features=[], data=None):
    if data is None:
        file_name = "./twitter_bots.arff"
        data = Matrix()

        data.load_arff(file_name)
        # TODO put this back?
        data.normalize()
        data.shuffle()
    num_train = int(data.rows * train_split)
    train_data = Matrix(data, 0, 0, num_train, data.cols)
    num_test = int(data.rows * (1.0 - train_split))
    test_data = Matrix(data, num_train, 0, data.rows - num_train, data.cols)

    train_x = {}
    test_x = {}
    for i in range(22):
        # if i == 15:
        #     continue
        if i not in remove_features:
        # if i not in remove_features:
            train_x["A{}".format(i + 1)] = np.array(train_data.col(i))
            test_x["A{}".format(i + 1)] = np.array(test_data.col(i))
    print(train_x.keys())
    
    train_y = np.array(train_data.col(22))
    test_y = np.array(test_data.col(22))

    return (train_x, train_y), (test_x, test_y), data

def train_input_fn(features, labels, batch_size):
    """An input function for training"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    # Return the dataset.
    return dataset

def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""
    features=dict(features)
    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)

    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    # Return the dataset.
    return dataset

