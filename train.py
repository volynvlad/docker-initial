from sklearn import datasets
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
# from lightgbm import LGBMClassifier

params =  {
            'boosting_type': 'dart',
            'max_depth' : 16,
            'num_leaves': 24,
            'nthread': -1,
            'learning_rate': 0.01,
            'subsample_freq': 1,
            'colsample_bytree': 0.9,
            'min_split_gain': 0.5,
            'min_child_weight': 1,
            'min_child_samples': 16,
            'n_estimators': 1000,
            'early_stopping_round': 10,
}

def train(classifier, params):
    iris = datasets.load_iris()
    iris_X = iris.data
    iris_y = iris.target

    np.random.seed(0)
    indices = np.random.permutation(len(iris_X))
    iris_X_train = iris_X[indices[:-10]]
    iris_y_train = iris_y[indices[:-10]]
    iris_X_test = iris_X[indices[-10:]]
    iris_y_test = iris_y[indices[-10:]]
    
    model = classifier(**params)
    print('Training model ...')
    model.fit(iris_X_train, iris_y_train)

    import joblib
    print('Saving model ...')
    joblib.dump(model, 'model.pkl')

# train(LGBMClassifier, params)
train(KNeighborsClassifier, {})