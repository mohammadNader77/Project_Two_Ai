import numpy as np
import csv
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier


TEST_SIZE = 0.3  # The proportion of the dataset to include in the test split
K = 3  # The number of nearest neighbors to consider for k-NN


# Define a class for the nearest neighbors model
class NN:
    def __init__(self, trainingFeatures, trainingLabels) -> None:
        self.trainingFeatures = trainingFeatures
        self.trainingLabels = trainingLabels

    def predict(self, features, k):
        """
        Given a list of features vectors of testing examples
        return the predicted class labels (list of either 0s or 1s)
        using the k nearest neighbors
        """
        neigh = KNeighborsClassifier(n_neighbors=k)
        neigh.fit(self.trainingFeatures, self.trainingLabels)
        return neigh.predict(features)


# Function to load data from a CSV file and convert it into features and labels
def load_data(filename):
    """
    Load spam data from a CSV file `filename` and convert into a list of
    features vectors and a list of target labels. Return a tuple (features, labels).

    features vectors should be a list of lists, where each list contains the
    57 features vectors

    labels should be the corresponding list of labels, where each label
    is 1 if spam, and 0 otherwise.
    """
    features = []
    labels = []
    with open(filename, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            features.append(row[:-1])  # Exclude the last column (labels)
            labels.append(int(row[-1]))  # Last column is the label
    return features, labels


# Function to preprocess the features by normalizing them
def preprocess(features):
    """
    Normalize each feature by subtracting the mean value in each
    feature and dividing by the standard deviation
    """
    scaler = StandardScaler()
    return scaler.fit_transform(features)


# Function to train an MLP model using the given features and labels
def train_mlp_model(features, labels):
    """
    Given a list of features lists and a list of labels, return a
    fitted MLP model trained on the data using the sklearn implementation.
    """
    model = MLPClassifier(
        hidden_layer_sizes=(10, 5), activation="logistic", max_iter=2000
    )

    model.fit(features, labels)
    return model


# Function to evaluate the performance of a model by computing various metrics
def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return (accuracy, precision, recall, f1).

    Assume each label is either a 1 (positive) or 0 (negative).
    """
    accuracy = accuracy_score(labels, predictions)
    precision = precision_score(labels, predictions)
    recall = recall_score(labels, predictions)
    f1 = f1_score(labels, predictions)
    return accuracy, precision, recall, f1


# Main function for executing the script
def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python template.py ./spambase.csv")

    # Load data from spreadsheet and split into train and test sets
    features, labels = load_data(sys.argv[1])
    features = preprocess(features)
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=TEST_SIZE
    )

    # Train a k-NN model and make predictions
    model_nn = NN(X_train, y_train)
    predictions = model_nn.predict(X_test, K)
    accuracy, precision, recall, f1 = evaluate(y_test, predictions)

    # Print results
    print("**** 1-Nearest Neighbor Results ****")
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1: ", f1)

    # Train an MLP model and make predictions
    model = train_mlp_model(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy, precision, recall, f1 = evaluate(y_test, predictions)

    # Print results
    print("**** MLP Results ****")
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1: ", f1)


# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()


# to run the code you must be to write the command in terminal : python Mohammad_1201369_Mohammad_1200937.py ./spambase.csv
