import logging
import numpy as np
import pandas as pd
from trader.indicadores.indicadores import Indicadores

class Tendencia(Indicadores):
    def __init__(self, name):
        super().__init__(name)
        self.max = 0
        self.min = 99999

    def resultados(self):
        logger.info("-"*80)
        logger.info("{} estadisticas".format(self))
        logger.info("Precio de cierre máximo value {}".format(self.max))
        logger.info("Precio de cierre mínimo value {}".format(self.min))

class MovingAverage(Tendencia):
    """ Media movil simple

    .. code: python

        df = MA(200)

    Args:
        df: pandas dataframe
        n: numero de periodos a tener en cuenta para calcular la MA.

    Return:
        Ultimo valor de la madia movil seleccionada.
    """
    def __init__(self, periods):
        self.name = "MA[{}]".format(periods)
        self.periods = periods
        self.max = 0
        self.min = 99999

    def calcular(self, df):
        ma = pd.Series(pd.Series.rolling(df['close'], self.periods).mean(), name=self)
        df[self] = ma
        try:
            v = ma.iloc[-1]
            value = 0 if str(np.nan) == str(v) else v
        except IndexError:
            value = 0
        self.max = value if value > self.max else self.max
        self.min = value if value < self.min and value != 0 else self.min
        return value
