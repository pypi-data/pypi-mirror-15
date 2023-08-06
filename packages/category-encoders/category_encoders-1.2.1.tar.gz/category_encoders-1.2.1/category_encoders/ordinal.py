"""

.. module:: ordinal
  :synopsis:
  :platform:

"""

import pandas as pd
import copy
from sklearn.base import BaseEstimator, TransformerMixin
import random
from category_encoders.utils import get_obj_cols

__author__ = 'willmcginnis'


def ordinal_encoding(X_in, mapping=None, cols=None):
    """
    Ordinal encoding uses a single column of integers to represent the classes. An optional mapping dict can be passed
    in, in this case we use the knowledge that there is some true order to the classes themselves. Otherwise, the classes
    are assumed to have no true order and integers are selected at random.

    :param X:
    :return:
    """

    X = X_in.copy(deep=True)

    if cols is None:
        cols = X.columns.values

    mapping_out = []
    if mapping is not None:
        for switch in mapping:
            for category in switch.get('mapping'):
                X.loc[X[switch.get('col')] == category[0], switch.get('col')] = str(category[1])

            X[switch.get('col')] = X[switch.get('col')].astype(int).reshape(-1, )
    else:
        for col in cols:
            categories = list(set(X[col].values))
            random.shuffle(categories)
            for idx, val in enumerate(categories):
                X.loc[X[col] == val, col] = str(idx)
            X[col] = X[col].astype(int).reshape(-1, )
            mapping_out.append({'col': col, 'mapping': [(x[1], x[0]) for x in list(enumerate(categories))]},)

    return X, mapping_out


class OrdinalEncoder(BaseEstimator, TransformerMixin):
    """
    Ordinal encoding uses a single column of integers to represent the classes. An optional mapping dict can be passed
    in, in this case we use the knowledge that there is some true order to the classes themselves. Otherwise, the classes
    are assumed to have no true order and integers are selected at random.
    """
    def __init__(self, verbose=0, mapping=None, cols=None, drop_invariant=False, return_df=True):
        """

        :param verbose: (optional, default=0) integer indicating verbosity of output. 0 for none.
        :param cols: (optional, default=None) a list of columns to encode, if None, all string columns will be encoded
        :param drop_invariant: (optional, default=False) boolean for whether or not to drop columns with 0 variance
        :param return_df: (optional, default=True) boolean for whether to return a pandas DataFrame from transform (otherwise it will be a numpy array)
        :return:
        """

        self.return_df = return_df
        self.drop_invariant = drop_invariant
        self.drop_cols = []
        self.verbose = verbose
        self.cols = cols
        self.mapping = mapping

    def fit(self, X, y=None, **kwargs):
        """
        Fit doesn't actually do anything in this case.  So the same object is just returned as-is.

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

        _, categories = ordinal_encoding(X, mapping=self.mapping, cols=self.cols)
        self.mapping = categories

        # drop all output columns with 0 variance.
        if self.drop_invariant:
            self.drop_cols = []
            X_temp = self.transform(X)
            self.drop_cols = [x for x in X_temp.columns.values if X_temp[x].var() <= 10e-5]

        return self

    def transform(self, X):
        """
        Will use the mapping (if available) and the column list (if available, otherwise every column) to encode the
        data ordinally.

        :param X:
        :return:
        """

        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        if not self.cols:
            return X

        X, _ = ordinal_encoding(X, mapping=self.mapping, cols=self.cols)

        if self.drop_invariant:
            for col in self.drop_cols:
                X.drop(col, 1, inplace=True)

        if self.return_df:
            return X
        else:
            return X.values