import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import load
class Detection_Weblog:
    def __init__(self):
        self.feature = {0: "cmdi", 1: "norm", 2: "path-traversal", 3: "sqli", 4: "xss"}
        self.model = self.load_model()
        self.vectorizer = self.load_tfidf()
    def load_model(self):
        model = tf.keras.models.load_model("model/cnn_detection.h5")
        return model
    def load_tfidf(self):
        tfidf = load("model/tfidf_vectorizer.joblib")
        return tfidf
    def detect(self, param):
        tfidf = self.vectorizer.transform(param)
        tfidf_dense = tfidf.toarray()
        tfidf_dense = tfidf_dense.reshape((tfidf_dense.shape[0], tfidf_dense.shape[1], 1))
        y_pred_prob = self.model.predict(tfidf_dense)
        y_pred = np.argmax(y_pred_prob, axis=1)
        return self.feature[y_pred[0]]


if(__name__ == "__main__"):
    detect = Detection_Weblog()
    print(detect.detect(["c/ caridad s/n"]))