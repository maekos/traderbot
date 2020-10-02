import logging
from datetime import time, datetime

logger = logging.getLogger('trader')


class Candle:
    def __init__(self, date: datetime = None, open: float=0.0, close: float=0.0,
                 high: float=0.0, low: float=0.0, volume: float=0):
        self.date = date
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
