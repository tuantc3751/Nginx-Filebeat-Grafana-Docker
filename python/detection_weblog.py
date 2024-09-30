import numpy as np
import tensorflow as tf
class Detection_Weblog:
    def __init__(self):
        self.feature = {0: "cmdi", 1: "norm", 2: "path-traversal", 3: "sqli", 4: "xss"}
        self.model = self.load_model()
    def load_model(self):
        model = tf.keras.models.load_model("model/cnn_detection.h5")
        return model

    def detect(self, param):
        y_pred_prob = self.model.predict(param)
        y_pred = np.argmax(y_pred_prob, axis=1)
        return self.feature[y_pred[0]]


if(__name__ == "__main__"):
    detect = Detection_Weblog()
    print(detect.detect(["c/ caridad s/n"]))