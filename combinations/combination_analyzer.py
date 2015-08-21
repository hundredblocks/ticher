from abc import abstractmethod
from cards import Cards

__author__ = 'marc.henri'

class CombinationAnalyzer():

    @staticmethod
    @abstractmethod
    def analyze(combination_cards: Cards):
        pass
