#!/usr/bin/env python3

import abc
import netaddr

import logging
__log__ = logging.getLogger(__name__)


class Converter(abc.ABC):
    def __init__(self, default):
        self.__default = default

    @property
    def default(self):
        return self.__default

    @abc.abstractmethod
    def encode(self, item):
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, item):
        raise NotImplementedError


class DictionaryConverter(Converter):
    def __init__(self, dictionary, default):
        super().__init__(default)
        self.__dictionary = dictionary

    @property
    def dictionary(self):
        return self.__dictionary

    def encode(self, item):
        return self.dictionary.get(item, self.dictionary.get(self.default))

    def decode(self, item):
        invert = {value: key for key, value in self.dictionary.items()}
        return invert.get(item, self.default)


class BooleanConverter(DictionaryConverter):
    def __init__(self, default=False):
        super().__init__({True: '1', False: '0'}, default)


class IntegerConverter(Converter):
    def __init__(self, default=None):
        super().__init__(default)

    def encode(self, item):
        assert isinstance(item, int)
        return str(item)

    def decode(self, item):
        return int(item)


class IPConverter(Converter):
    def __init__(self, default=None):
        super().__init__(default)

    def encode(self, item):
        return str(item)

    def decode(self, item):
        return netaddr.IPAddress(item)


class MACConverter(Converter):
    def __init__(self, default=None):
        super().__init__(default)

    def encode(self, item):
        return str(item)

    def decode(self, item):
        return netaddr.EUI(item)
