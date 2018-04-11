"""An Example of a DNNClassifier for the Iris dataset."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import tensorflow as tf
import sys

import data_extractor


parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=100, type=int, help='batch size')
parser.add_argument('--train_steps', default=1000, type=int,
                    help='number of training steps')


def main(argv):
    args = parser.parse_args(argv[1:])
    data_extractor.prep_load_data()
    data = None

    best_remove_attr = []
    cur_remove_attr = []

    temp = []
    temp.append(calc_accuracy(args, [15, 5, 2, 3, 20, 12, 10, 16])[0])
    temp.append(calc_accuracy(args, [15, 5])[0])
    temp.append(calc_accuracy(args, [15, 5, 2, 3, 20, 12, 10, 6])[0])
    temp.append(calc_accuracy(args, [15, 20, 1, 6, 5, 16, 11, 9, 21])[0])
    temp.append(calc_accuracy(args, [15, 20, 1, 6, 5, 16, 11, 9, 12])[0])
    temp.append(calc_accuracy(args, [15, 5, 11, 6, 9, 12])[0])
    print("Results: {}".format(temp))
    sys.exit(0)

    print("\nCalculating with exclude set of: {}\n".format(best_remove_attr))
    best_accuracy, data = calc_accuracy(args, best_remove_attr)
    orig_accuracy = best_accuracy
    # cur_accuracy = 0.0
    # while cur_accuracy >= best_accuracy:
    while True:
        print("Here we go again")
        for attr in range(22):
            if attr not in cur_remove_attr:
                # best_inner_remove_attr = 
                exclude_attr = cur_remove_attr[:]
                exclude_attr.append(attr)
                print("\nCalculating with exclude set of: {}\n".format(exclude_attr))
                accuracy, _ = calc_accuracy(args, exclude_attr, data)
                if accuracy >= best_accuracy:
                    best_accuracy = accuracy
                    best_remove_attr = exclude_attr[:]

        # TODO check if took away attribute and still had exact same accuracy
        # if orig_accuracy == best_accuracy or len(best_remove_attr) > 20:
        if orig_accuracy > best_accuracy or len(best_remove_attr) > 20:
            # TODO test this
            # didn't change
            break
        else:
            cur_remove_attr = best_remove_attr[:]
            orig_accuracy = best_accuracy
        # TODO remove this
        # break

    # TODO which of these do I use
    print("Best exclude attributes: {}".format(cur_remove_attr))
    print("Best exclude attributes: {}".format(best_remove_attr))
    print("Best accuracy: {}".format(best_accuracy))
    print("Best accuracy: {}".format(orig_accuracy))

def calc_accuracy(args, attr_exclude_list, data=None):

    # Fetch the data
    # (train_x, train_y), (test_x, test_y) = data_extractor.load_data()
    # (train_x, train_y), (test_x, test_y) = data_extractor.load_data(0.9)
    (train_x, train_y), (test_x, test_y), data = data_extractor.load_data(0.1, attr_exclude_list, data)
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
    # print("result: {}".format(eval_result))
    return eval_result["accuracy"], data

if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)
