import logging

from trader.candle import Candle

logger = logging.getLogger('trader')


class Ticker():
    def __init__(self, nombre):
        self.nombre = nombre
        self.candle = Candle()
