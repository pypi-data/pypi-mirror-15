"""

.. module:: sum_coding
  :synopsis:
  :platform:

"""

import copy
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from patsy.highlevel import dmatrix
from category_encoders.ordinal import OrdinalEncoder
from category_encoders.utils import get_obj_cols

__author__ = 'willmcginnis'


def sum_coding(X_in, cols=None):
    """

    :param X:
    :return:
    """

    X = copy.deepcopy(X_in)

    if cols is None:
        cols = X.columns.values
        pass_thru = []
    else:
        pass_thru = [col for col in X.columns.values if col not in cols]

    bin_cols = []
    for col in cols:
        mod = dmatrix("C(%s, Sum)" % (col, ), X)
        for dig in range(len(mod[0])):
            X[col + '_%d' % (dig, )] = mod[:, dig]
            bin_cols.append(col + '_%d' % (dig, ))

    X = X.reindex(columns=bin_cols + pass_thru)

    return X


class SumEncoder(BaseEstimator, TransformerMixin):
    """

    """
    def __init__(self, verbose=0, cols=None, drop_invariant=False):
        """

        :param verbose:
        :param cols:
        :return:
        """

        self.drop_invariant = drop_invariant
        self.drop_cols = []
        self.verbose = verbose
        self.cols = cols
        self.ordinal_encoder = OrdinalEncoder(verbose=verbose, cols=cols)

    def fit(self, X, y=None, **kwargs):
        """

        :param X:
        :param y:
        :param kwargs:
        :return:
        """

        # if the input dataset isn't already a dataframe, convert it to one (using default column names)
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        # if columns aren't passed, just use every string column
        if self.cols is None:
            self.cols = get_obj_cols(X)

        self.ordinal_encoder = self.ordinal_encoder.fit(X)

        # train an ordinal pre-encoder
        self.ordinal_encoder = self.ordinal_encoder.fit(X)

        # drop all output columns with 0 variance.
        if self.drop_invariant:
            self.drop_cols = []
            X_temp = self.transform(X)
            self.drop_cols = [x for x in X_temp.columns.values if X_temp[x].var() <= 10e-5]

        return self

    def transform(self, X):
        """

        :param X:
        :return:
        """

        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        X = self.ordinal_encoder.transform(X)

        X = sum_coding(X, cols=self.cols)

        if self.drop_invariant:
            for col in self.drop_cols:
                X.drop(col, 1, inplace=True)

        return X