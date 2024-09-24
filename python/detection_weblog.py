from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
class Detection_Weblog:
    def __init__(self):
        self.feature = {0: "cmdi", 1: "norm", 2: "path-traversal", 3: "sqli", 4: "xss"}
        self.load_pca_model()
        self.load_nonpca_model()
    
    def load_pca_model(self):
        # self.pca_vectorizer = TfidfVectorizer(min_df=0.0, analyzer="char", sublinear_tf=True, ngram_range=(3, 3), max_features=8000)
        # self.pca_pca = PCA(n_components=256)
        # self.pca_smote = SMOTE()
        # self.pca_rf_classifier = RandomForestClassifier(n_estimators=50)
        self.pca_vectorizer = joblib.load('model/tfidf_vectorizer.pkl')
        self.pca_pca = joblib.load('model/pca_model.pkl')
        self.pca_rf_classifier = joblib.load('model/random_forest_model.pkl')
    def load_nonpca_model(self):
        # self.nonpca_vectorizer = TfidfVectorizer(min_df=0.0, analyzer="char", sublinear_tf=True, ngram_range=(3, 3), max_features=8000)
        # self.nonpca_smote = SMOTE()
        # self.nonpca_rf_classifier = RandomForestClassifier(n_estimators=50)
        self.nonpca_vectorizer = joblib.load('model/tfidf_vectorizer_nonpca.pkl')
        self.nonpca_rf_classifier = joblib.load('model/random_forest_model_nonpca.pkl')

    def detect(self, param, mode):
        if(mode == "pca"):
            tfidf = self.pca_vectorizer.transform(param)
            reduced  = self.pca_pca.transform(tfidf.toarray())
            y_pred = self.pca_rf_classifier.predict(reduced)
            # print(y_pred[0])
            return self.feature[y_pred[0]]
        else:
            tfidf = self.nonpca_vectorizer.transform(param)
            # reduced  = self.pca_pca.transform(tfidf.toarray())
            y_pred = self.nonpca_rf_classifier.predict(tfidf)
            # print(y_pred)
            return self.feature[y_pred[0]]

if(__name__ == "__main__"):
    detect = Detection_Weblog()
    print(detect.detect(["c/ caridad s/n"], "pca"))