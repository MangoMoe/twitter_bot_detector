from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import graphviz

from matrix import Matrix
import numpy as np

##### Twitter dataset
print("\n\nTwitter dataset\n")

file_name = "/home/drc95/Documents/school/478cs/twitterbotcs478/twitter_bots_altered.arff"
data = Matrix()
data.load_arff(file_name)

data.shuffle()
# data.normalize()

# train_proportion = 0.7
train_proportion = 0.9
test_proportion = 1.0 - train_proportion

num_train = int(data.rows * train_proportion)
train_data = Matrix(data, 0, 0, num_train, data.cols)
num_test = int(data.rows * test_proportion)
test_data = Matrix(data, num_train, 0, data.rows - num_train, data.cols)
# test_data = Matrix(data, num_train, 0, data.rows - num_test, data.cols)

train_features = Matrix(train_data, 0, 0, train_data.rows, train_data.cols-1)
train_labels = Matrix(train_data, 0, train_data.cols-1, train_data.rows, 1)

test_features = Matrix(test_data, 0, 0, test_data.rows, test_data.cols-1)
test_labels = Matrix(test_data, 0, test_data.cols-1, test_data.rows, 1)

print("Num training instances: {}".format(train_data.rows))
print("Num test instances: {}".format(test_data.rows))

class_names = ["Bot", "User"]
feature_names = [
    # "Average Number of Tweets",
    # "Contributors Enables",
    # "Default Profile",
    # "Default Profile Image",
    # "Favorite Average",
    # "Favorites Count",
    # "Followers Count",
    # "Friends Count",
    # "Hashtags Average",
    # "Listed Count",
    # "Media Average",
    # "Protected",
    # "Quote Average",
    # "Reply Average",
    # "Retweet Average",
    # "Statuses Count",
    # "Symbols Average",
    # "Tweet Regularity",
    # "URL",
    # "URLs Average",
    # "User Mentions Average",
    # "Verified"

    "Average Tweets per Day",
    "Contributors Enabled",
    "Default Profile Settings Enabled",
    "Default Profile Image Enabled",
    "Total Number of Favorites",
    "Total Number of Followers",
    "Number of Friends",
    "Listed Count",
    "Average Hashtags per Tweet",
    "Account is Protected",
    "Average Media Count per Tweet",
    "Average Favorites per Tweet",
    "Averages Quotes per Tweet",
    "Average Replys per Tweet",
    "Average Retweets",
    "Average URLs per Tweet",
    "Average User Mentions per Tweet",
    "Average Symbols per Tweet",
    "Total Statuses Count",
    "Tweet Regularity",
    "Has a custom URL",
    "Verified Twitter Account"
]

# decision_tree = tree.DecisionTreeClassifier()
# decision_tree = tree.DecisionTreeClassifier(max_features=7)
# decision_tree = tree.DecisionTreeClassifier(max_features=3)
decision_tree = tree.DecisionTreeClassifier(max_leaf_nodes=10)
decision_tree = decision_tree.fit(train_features.data, train_labels.col(0))

score = decision_tree.score(test_features.data, test_labels.col(0))
print("Accuracy was: {}".format(score))

# dot_data = tree.export_graphviz(decision_tree, out_file=None, 
#                          feature_names=feature_names,  
#                          class_names=class_names,  
#                          filled=True, rounded=True,  
#                          special_characters=True) 

dot_data = tree.export_graphviz(decision_tree, out_file=None, 
                         feature_names=feature_names,  
                         class_names=class_names,  
                         filled=True, rounded=True,  
                         special_characters=True,
                         max_depth=4,
                         label="root",
                         impurity=False,
                         proportion=True) 

graph = graphviz.Source(dot_data)
# graph.render("DecisionTree_Twitter")
graph.render("DecisionTree_Twitter_Pruned")

# rand_forest = RandomForestClassifier()
# rand_forest = rand_forest.fit(train_features.data, train_labels.col(0))
#
# score = rand_forest.score(test_features.data, test_labels.col(0))
# print("Accuracy was: {}".format(score))
# importance = rand_forest.feature_importances_
# # print()
# for i in range(len (importance)):
#     # print("{}: {}".format(i + 1, importance[i]))
#     print("{}: {}".format(i + 2, importance[i]))
