import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def leer_excel(filename):
    """ Guarda en un dataframe datos leidos de un archivo excel

    Args:
        filename: ruta al archivo a leer
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError
    if not filename.endswith('.xlsx'):
        raise ValueError
    data = pd.read_excel(filename)
    data = data.sort_values('timestamp', ascending=True)
    data.set_index('timestamp', inplace=True)
    return data
