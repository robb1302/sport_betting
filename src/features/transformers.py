from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


"""
Klasse wird noch nicht verwendet
"""

class addDericedBookmakerPred(BaseEstimator, TransformerMixin):
    def __init__(self, bookmaker):
        self.bookmaker = bookmaker
    def fit(self, X, y = None):
        return self
    def transform(self, X):
        odds_pred = get_odd_pred(bet=self.bookmaker,df=X)
        X_prep = X.join(odds_pred)
        return X_prep

class addDericedBookmakerOdds(BaseEstimator, TransformerMixin):
    def __init__(self, bookmakers):
        bookmaker_attributes = []
        for bm in bookmakers:
            bookmaker_attributes += get_bookmaker(bm = bm,df = df)
        
        self.bookmaker_attributes = bookmaker_attributes
    def fit(self, X, y = None):
        return self
    def transform(self, X):
        bet_on_team = get_bookmaker(bm='Team',df=df[bookmaker_attributes])
        odds_pred = derived_odds(sight = 'Team',df=df, odds=bet_on_team)
        X_prep = X.join(odds_pred)
        return X_prep