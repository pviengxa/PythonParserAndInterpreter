from abc import ABC, ABCMeta, abstractmethod


class abstractStatement(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def evaluate(self): pass


class abstractArithmeticExpression(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def evaluate(self): pass
