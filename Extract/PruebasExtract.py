import requests
import pandas as pd
import numpy as np

class PruebaEstractor:

    def __init__(self, csv_paht):
        self.csv_paht = csv_paht

    def queries(self):
        data = pd.read_csv(self.csv_paht)

    def response():
        return data.head(5)
