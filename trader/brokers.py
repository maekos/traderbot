import abc
import logging
import requests
import pandas as pd
import yfinance as yf
from datetime import time, datetime

from trader.ticker import Ticker
from trader.candle import Candle
from trader.mercados import Mercado
from trader.mercados import MercadoDummy
from trader.mercados import MervalDummy

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
    def historico(cls, ticker: Ticker, start='2020-01-01', end='2020-09-28'):
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


class IOL:
    """
    API invertir online
    iol = IOL(token)
    iol.historico("GGAL", start="2015-01-01", end="2019-05-05", Aj=True)
    # Necesita token
    portafolio = iol.mi_portafolio()
    """

    API_URL = 'https://api.invertironline.com/api/v2/'
    URL = 'https://www.invertironline.com'


    def __init__(self, token=None, mercado: Mercado = MercadoDummy()):
        self.token = token
        self.mercado = mercado

    def ticker_id(self, ticker: Ticker):
        URL_ID_TICKER = '{}/api/cotizaciones/idtitulo?simbolo={}&mercado={}'.format(self.URL,
                                                                                    ticker.nombre,
                                                                                    self.mercado.nombre)
        id_titulo = requests.get(url=URL_ID_TICKER)
        _id = str(id_titulo.text)
        return _id

    def mi_portafolio(self):
        """ Portafolio

        Devuelve el portafolio de IOL
        Esta consulta necesita del token.

        """
        portafolio = '{}/portafolio/argentina'.format(self.API_URL)
        headers = {"Authorization" : "Bearer " + self.token}
        data = requests.get(url=portafolio, headers=headers).json()
        return data

    def historico(self, ticker: Ticker, start, end, ajustado=False):
        ajuste = 'ajustada' if ajustado else 'sinAjustar'
        endpoint= "{}/Titulos/{}/Cotizacion/seriehistorica/{}/{}/{}".format(
            self.mercado.nombre, ticker.nombre, start, end, ajuste)
        url = self.API_URL + endpoint
        headers = {"Authorization" : "Bearer " + self.token}
        data = requests.get(url=url, headers=headers).json()

        tabla = pd.DataFrame(data).set_index("fechaHora")
        tabla.index = pd.to_datetime(tabla.index)
        tabla = tabla.resample("d").last()
        tabla = tabla.drop(["moneda", "interesesAbiertos", "puntas"], axis=1)
        return tabla.dropna()

    def intradiario(self, ticker: Ticker):
        """ Cotizaciones del día

        Según el ticker pasado como parámetro devuelve
        """
        url = "{}/Titulo/GraficoIntradiario?idTitulo={}&idTipo=4&idMercado=1".format(self.URL, _id)
        data = requests.get(url, headers={'idTitulo': self.ticker_id(ticker), 'idTipo': '4', 'idMercado': '1'}).json()
        tabla = pd.DataFrame(data)
        ticker.candle.open = tabla['Ultima'].iloc[0]
        ticker.candle.close = tabla['Ultima'].iloc[-1]
        ticker.candle.high = max(tabla['Ultima'])
        ticker.candle.low = min(tabla['Ultima'])
        ticker.candle.volume = sum(tabla['CantidadNominal'])
        return tabla
