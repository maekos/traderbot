import abc
import logging

logger = logging.getLogger('trader')


class DataBase(abc.ABC):

    @abc.abstractmethod
    def push(self, ticker):
        """ Guarda los datos a la base de datos
        """

    @abc.abstractmethod
    def get(self, ticker):
        """ Recupera el ticker de la base de datos
        """
