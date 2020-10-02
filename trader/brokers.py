import abc
import logging
import yfinance as yf
from datetime import time, datetime

from trader.ticker import Ticker
from trader.candle import Candle
from trader.mercados import Mercado
from trader.mercados import MercadoDummy

logger = logging.getLogger('trader')


class Broker(abc.ABC):
    def __init__(self, nombre, mercado: Mercado):
        self.nombre = nombre
        self.mercado = mercado

    @abc.abstractmethod
    def get(self, ticker: str) -> Ticker:
        """ Devuelve información de precio del simbolo pasado como parametro

        Returns:
            Objeto del tipo Vela con los valores HOLC
        """


class YahooFinance(Broker):
    def __init__(self, data=None, mercado: Mercado = MercadoDummy()):
        super().__init__(self.__class__.__name__, mercado)
        self.iterator = 0
        self.table = data

    @classmethod
    def from_yahoo(cls, ticker: Ticker, start='2020-01-01', end='2020-09-28'):
        data = yf.download(ticker.nombre, start=start, end=end)
        return cls(data)

    def get(self, ticker: Ticker) -> Ticker:
        try:
            data = self.table.iloc[self.iterator]
            date = str(self.table.index.values[self.iterator])
        except IndexError:
            raise StopIteration('No hay mas datos')
        self.iterator += 1
        ticker.candle = Candle(date,
                               data['Open'],
                               data['Close'],
                               data['High'],
                               data['Low'],
                               data['Volume'])
        return ticker
