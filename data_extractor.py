import pandas as pd
import tensorflow as tf
from matrix import Matrix
import numpy as np



def load_data(train_split=0.7):
    file_name = "./twitter_bots.arff"
    data = Matrix()

    data.load_arff(file_name)
    data.shuffle()
    num_train = int(data.rows * train_split)
    train_data = Matrix(data, 0, 0, num_train, data.cols)
    num_test = int(data.rows * (1.0 - train_split))
    test_data = Matrix(data, num_train, 0, data.rows - num_train, data.cols)

    train_x = {}
    train_x["A1"] = np.array(train_data.col(0))
    train_x["A2"] = np.array(train_data.col(1))
    train_x["A3"] = np.array(train_data.col(2))
    train_x["A4"] = np.array(train_data.col(3))
    train_x["A5"] = np.array(train_data.col(4))
    train_x["A6"] = np.array(train_data.col(5))
    train_x["A7"] = np.array(train_data.col(6))
    train_x["A8"] = np.array(train_data.col(7))
    train_x["A9"] = np.array(train_data.col(8))
    train_x["A10"] = np.array(train_data.col(9))
    train_x["A11"] = np.array(train_data.col(10))
    train_x["A12"] = np.array(train_data.col(11))
    train_x["A13"] = np.array(train_data.col(12))
    train_x["A14"] = np.array(train_data.col(13))
    train_x["A15"] = np.array(train_data.col(14))
    train_x["A16"] = np.array(train_data.col(15))
    train_x["A17"] = np.array(train_data.col(16))
    train_x["A18"] = np.array(train_data.col(17))
    train_x["A19"] = np.array(train_data.col(18))
    train_x["A20"] = np.array(train_data.col(19))
    train_x["A21"] = np.array(train_data.col(20))
    train_x["A22"] = np.array(train_data.col(21))

    train_y = np.array(train_data.col(22))
    
    test_x = {}
    test_x["A1"] = np.array(test_data.col(0))
    test_x["A2"] = np.array(test_data.col(1))
    test_x["A3"] = np.array(test_data.col(2))
    test_x["A4"] = np.array(test_data.col(3))
    test_x["A5"] = np.array(test_data.col(4))
    test_x["A6"] = np.array(test_data.col(5))
    test_x["A7"] = np.array(test_data.col(6))
    test_x["A8"] = np.array(test_data.col(7))
    test_x["A9"] = np.array(test_data.col(8))
    test_x["A10"] = np.array(test_data.col(9))
    test_x["A11"] = np.array(test_data.col(10))
    test_x["A12"] = np.array(test_data.col(11))
    test_x["A13"] = np.array(test_data.col(12))
    test_x["A14"] = np.array(test_data.col(13))
    test_x["A15"] = np.array(test_data.col(14))
    test_x["A16"] = np.array(test_data.col(15))
    test_x["A17"] = np.array(test_data.col(16))
    test_x["A18"] = np.array(test_data.col(17))
    test_x["A19"] = np.array(test_data.col(18))
    test_x["A20"] = np.array(test_data.col(19))
    test_x["A21"] = np.array(test_data.col(20))
    test_x["A22"] = np.array(test_data.col(21))

    test_y = np.array(test_data.col(22))

    return (train_x, train_y), (test_x, test_y)

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

