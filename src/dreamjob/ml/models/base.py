from typing import Protocol


class BaseModel(Protocol):
    def __init__(self):
        self.name = None

    def fit(self, X):
        ...

    def transform(self, X):
        ...

    def predict(self, user_input):
        ...

    def save_model(self):
        ...

    def load_artifacts(self):
        ...
