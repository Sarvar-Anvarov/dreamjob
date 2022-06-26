import pickle
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from dreamjob.config import settings
from dreamjob.commons.data_models import Recommendation, Recommendations


class TFIDFModel:
    def __init__(self, model=None):
        self.name = "tf_idf"
        self.model = model
        self.matrix = None

    def fit(self, X):
        self.model = TfidfVectorizer()
        self.model.fit(X)
        return self

    def transform(self, X):
        return self.model.transform(X)

    def predict(self, user_input):
        user_vector = self.model.transform([user_input])
        idx = np.argsort(cosine_similarity(user_vector, self.matrix))[0][-6:-1]

        return Recommendations(
            recommendations=[
                Recommendation(**{"id": v})
                for v in idx
            ]
        )

    def save_model(self):
        pickle.dump(self.model, open("tf_idf.p", "wb"))

    def load_artifacts(self):
        self.model = pickle.load(open(settings.TF_IDF.model, "rb"))
        self.matrix = pickle.load(open(settings.TF_IDF.matrix, "rb"))
        return self
