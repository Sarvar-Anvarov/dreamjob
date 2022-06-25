import pandas as pd


def preprocess(text):
    return text.str.to_lower()
