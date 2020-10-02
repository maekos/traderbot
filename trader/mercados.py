import pytz
import logging
from datetime import time, datetime

logger = logging.getLogger('trader')

logger.setLevel(logging.DEBUG)


class MercadoCerrado(Exception):
    pass


class Mercado:
    """
    """
    tz = pytz.timezone('America/Argentina/Cordoba')

    def __init__(self, nombre: str, apertura: time, cierre: time):
        self.nombre = nombre
        self.apertura = apertura
        self.cierre = cierre

    def is_open(self):
        tm = datetime.now(tz=None).time()
        if tm >= self.apertura and tm <= self.cierre:
            return True
        return False

    def seconds_for_close(self):
        if not self.is_open():
            logger.debug("{} is closed".format(self.__class__.__name__))
            raise MercadoCerrado
        tm = datetime.now(tz=self.tz).time()
        return (datetime.combine(datetime.today(), self.cierre) -
                datetime.combine(datetime.today(), tm)).seconds


class MercadoDummy(Mercado):
    def __init__(self):
        super().__init__('Dummy', time(0, 0, 0), time(23, 59, 59))
