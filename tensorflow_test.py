"""An Example of a DNNClassifier for the Iris dataset."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import tensorflow as tf

import data_extractor


parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=100, type=int, help='batch size')
parser.add_argument('--train_steps', default=1000, type=int,
                    help='number of training steps')


def main(argv):
    args = parser.parse_args(argv[1:])

    # Fetch the data
    # (train_x, train_y), (test_x, test_y) = data_extractor.load_data()
    # (train_x, train_y), (test_x, test_y) = data_extractor.load_data(0.9)
    (train_x, train_y), (test_x, test_y) = data_extractor.load_data(0.1)
    # (train_x, train_y), (test_x, test_y) = data_extractor.load_data(0.05)

    # Feature columns describe how to use the input.
    my_feature_columns = []
    for key in train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))

    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 10 nodes each.
        # hidden_units=[10, 10],
        # hidden_units=[30, 30, 30],
        # hidden_units=[100] * 20,
        hidden_units=[100] * 3,
        # hidden_units=[1024] * 5,
        # hidden_units=[1024, 512, 256],
        # The model must choose between 2 classes.
        n_classes=2)

    # classifier = tf.estimator.DNNClassifier(
    #     feature_columns=my_feature_columns,
    #     hidden_units=[1024, 512, 256])

    # classifier = tf.estimator.DNNClassifier(
    #     feature_columns=my_feature_columns,
    #     hidden_units=[1024, 512, 256],
    #     optimizer=tf.train.ProximalAdagradOptimizer(
    #       learning_rate=0.1,
    #       l1_regularization_strength=0.001
    #     ))

    # Train the Model.
    classifier.train(
        input_fn=lambda:data_extractor.train_input_fn(train_x, train_y,
                                                 args.batch_size),
        steps=args.train_steps)

    # Evaluate the model.
    eval_result = classifier.evaluate(
        input_fn=lambda:data_extractor.eval_input_fn(test_x, test_y,
                                                args.batch_size))

    print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)
