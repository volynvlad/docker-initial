from sklearn import datasets
import numpy as np


def train():
    iris = datasets.load_iris()
    iris_X = iris.data
    iris_y = iris.target

    np.random.seed(0)
    indices = np.random.permutation(len(iris_X))
    iris_X_train = iris_X[indices[:-10]]
    iris_y_train = iris_y[indices[:-10]]
    iris_X_test = iris_X[indices[-10:]]
    iris_y_test = iris_y[indices[-10:]]

    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier()
    print('Training model ...')
    knn.fit(iris_X_train, iris_y_train)

    import joblib
    print('Saving model ...')
    joblib.dump(knn, 'knn.pkl')

train()