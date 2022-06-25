import pickle
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TFIDFModel:
    def __init__(self, model=None):
        self.model = model

    def fit(self, X):
        self.model = TfidfVectorizer()
        self.model.fit(X)
        return self

    def transform(self, X):
        return self.model.transform(X)

    def predict(self, user_input, sparce_matrix):
        user_vector = self.model.transform([user_input])
        idx = np.argsort(cosine_similarity(user_vector, sparce_matrix))[0][-6:-1]
        return {"vacancies": idx}

    def save_model(self):
        pickle.dump(self.model, open("tf_idf.p", "wb"))
