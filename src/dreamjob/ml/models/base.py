from typing import Protocol


class BaseModel(Protocol):
    def fit(self, X):
        ...

    def transform(self, X):
        ...

    def save_model(self):
        ...
