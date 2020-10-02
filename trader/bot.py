import time
import logging
import threading
import pandas as pd

from trader.brokers import Broker
from trader.ticker import Ticker
from trader.database import DataBase

logger = logging.getLogger('trader')


class Bot(threading.Thread):

    def __init__(self, ticker: Ticker, broker: Broker,
                 database: DataBase = None, estrategias: list = None, timing: int = 1):
        self.ticker = ticker
        self.broker = broker
        self.database = database
        self.timing = timing
        self.estrategias = estrategias
        self.dataframe = pd.DataFrame(columns=['date', 'open', 'close', 'high', 'low', 'volume'])
        super().__init__(name=ticker.nombre)

    def run(self):
        while self.broker.mercado.is_open():
            try:
                try:
                    self.broker.get(self.ticker)
                except TypeError:
                    logger.error('Bad return value from broker')
                    time.sleep(self.timing)
                    continue
                logger.info('<{}> date <{}> open: {}, close {}, high {}, low {} volume:{}'.format(
                    self.ticker.nombre,
                    self.ticker.candle.date,
                    self.ticker.candle.open,
                    self.ticker.candle.close,
                    self.ticker.candle.high,
                    self.ticker.candle.low,
                    self.ticker.candle.volume))
                self.dataframe = self.dataframe.append(self.ticker.candle.__dict__,
                                                       ignore_index=True)
                if self.estrategias is not None:
                    for estrategia in self.estrategias:
                        self.estrategias.analizar(self.dataframe)
            except StopIteration:
                logger.info("Trader bot finalizado")
                if self.estrategias is not None:
                    for estrategia in self.estrategias:
                        self.estrategia.estadisticas()
                break
            if self.database is not None:
                self.database.push()
            time.sleep(self.timing)
