import pandas as pd
from .models import Disasterchatbot

def load_data():
    df = pd.read_csv('disasters.csv')
    for _, row in df.iterrows():
        Disasterchatbot.objects.create(
            name=row['DisasterName'],
            description=row['Description'],
            causes=row['Causes'],
            precautions=row['Precautions'],
            reference_link=row['ReferenceLinks']
        )
