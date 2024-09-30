
import numpy as np
import urllib.parse as parse
import re
import json
from detection_weblog import Detection_Weblog
def preprocess_url(url):
    # Preprocess URL before inference
    decoded_url = parse.unquote(url).lower()
    clean_url = decoded_url.strip()
    if(len(clean_url.split()) == 1):  
        return " ".join(clean_url.split())
    return " ".join(clean_url.split()[1:])

model = Detection_Weblog()

def predict_single_url(url):
    # Preprocess the URL and prepare it for inference
    
    preprocessed_url = preprocess_url(url)
    if(len(preprocessed_url) == 0):
        return "none"
    print([preprocessed_url])
    print(model.detect([preprocessed_url]))
    return model.detect(preprocessed_url)
    # Make prediction
    # prediction = model.predict(padded)
    # if (prediction[0][0] > 0.8):
    #     return "attack"
    # else:
    #     return "none"
    

        
