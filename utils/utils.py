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

def ajustar_cierre(df):
    df['factor'] = df.adjusted_close / df.close
    df['VolMlnUSD'] = df.close * df.volume / 1000000
    cols = [df.open * df.factor,
            df.high * df.factor,
            df.low * df.factor,
            df.adjusted_close,
            df.VolMlnUSD]
    dataAj = pd.concat(cols, axis=1)
    dataAj.columns = ['Open', 'High', 'Low', 'Close', 'VolMlnUSD']
    return dataAj.round(2)

def graficar_correlacion(df, title=''):
    fig = plt.figure(figsize=(12, 8))
    plt.matshow(df, fignum=fig.number, cmap='binary')
    plt.xticks(range(df.shape[1]), df.columns, fontsize=12, rotation=90)
    plt.yticks(range(df.shape[1]), df.columns, fontsize=12)

    cb = plt.colorbar(orientation='vertical', label="Factor de correlación 'r'")
    cb.ax.tick_params(labelsize=12)
    plt.title(title, fontsize=16, y=1.15)

    ax = plt.gca()

    ax.set_xticks(np.arange(-.5, len(df), 1), minor=True);
    ax.set_yticks(np.arange(-.5, len(df), 1), minor=True);
    ax.grid(which='minor', color='w', linestyle='-', linewidth=3)

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if df.iloc[i,j] > 0.6:
                color = 'white'
            else:
                color = 'black'
            fig.gca().text(i, j, "{:.2f}".format(df.iloc[i,j]), ha='center', va='center', c = color, size=14)
    return plt
