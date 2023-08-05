# Sebastian Raschka 2014-2016
# mlxtend Machine Learning Library Extensions
#
# Base Clusteer (Clutering Parent Class)
# Author: Sebastian Raschka <sebastianraschka.com>
#
# License: BSD 3 clause

import numpy as np
from ._base_supervised_estimator import _BaseSupervisedEstimator


class _BaseClassifier(_BaseSupervisedEstimator):

    """Parent Class Classifier

    A base class that is implemented by classifiers

    """
    def __init__(self, print_progress=0, random_seed=0):
        super(_BaseClassifier, self).__init__(
            print_progress=print_progress,
            random_seed=random_seed)
        self._binary_classifier = False

    def _check_target_array(self, y, allowed=None):
        if not np.issubdtype(y[0], int):
            raise AttributeError('y must be an integer array.\nFound %s'
                                 % y.dtype)
        found_labels = np.unique(y)
        if (found_labels < 0).any():
            raise AttributeError('y array must not contain negative labels.'
                                 '\nFound %s' % found_labels)
        if allowed is not None:
            found_labels = tuple(found_labels)
            if found_labels not in allowed:
                raise AttributeError('Labels not in %s.\nFound %s'
                                     % (allowed, found_labels))

    def score(self, X, y):
        """ Compute the prediction accuracy

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples and
            n_features is the number of features.
        y : array-like, shape = [n_samples]
            Target values (true class labels).

        Returns
        ---------
        acc : float
            The prediction accuracy as a float
            between 0.0 and 1.0 (perfect score).

        """
        y_pred = self.predict(X)
        acc = np.sum(y == y_pred, axis=0) / float(X.shape[0])
        return acc
