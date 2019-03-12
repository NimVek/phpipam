#!/usr/bin/env python3

import abc
import datetime
import netaddr

import logging
__log__ = logging.getLogger(__name__)


class Converter(abc.ABC):
    @abc.abstractmethod
    def encode(self, item):
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, item):
        raise NotImplementedError

    def __call__(self,item):
        if isinstance(item,str):
           return self.decode(item)
        else:
           return self.encode(item)

class DefaultConverter(Converter):
    def __init__(self, default):
        self.__default = default

    @property
    def default(self):
        return self.__default

    @abc.abstractmethod
    def _encode(self, item):
        raise NotImplementedError

    @abc.abstractmethod
    def _decode(self, item):
        raise NotImplementedError

    def encode(self, item):
        if item is None:
          return None
        else:
         try:
          return self._encode(item)
         except:
          return self._encode(self.default)

    def decode(self, item):
        if item is None:
          return self.default
        try:
          return self._decode(item)
        except:
          return self.default

class TypeConverter(DefaultConverter):
    def __init__(self,typ,default):
      super().__init__(default)
      self.__type = typ

    @property
    def type(self):
        return self.__type

    def _encode(self, item):
        assert isinstance(item,self.type)
        return str(item)

    def _decode(self, item):
        return self.type(item)


class DictionaryConverter(DefaultConverter):
    def __init__(self, dictionary, default):
        super().__init__(default)
        self.__dictionary = dictionary

    @property
    def dictionary(self):
        return self.__dictionary

    def _encode(self, item):
        return self.dictionary[item]

    def _decode(self, item):
        invert = {value: key for key, value in self.dictionary.items()}
        return invert[item]


class BooleanConverter(DictionaryConverter):
    def __init__(self, default=False):
        super().__init__({True: '1', False: '0'}, default)

class YesNoConverter(DictionaryConverter):
    def __init__(self, default=False):
        super().__init__({True: 'Yes', False: 'No'}, default)

class IntegerConverter(TypeConverter):
    def __init__(self, default=None):
        super().__init__(int, default)

class StringConverter(TypeConverter):
    def __init__(self, default=None):
        super().__init__(str, default)

class IPConverter(TypeConverter):
    def __init__(self, default=None):
        super().__init__(netaddr.IPAddress,default)

class MACConverter(DefaultConverter):
    def __init__(self, default=None):
        super().__init__(default)

    def _encode(self,item):
       item.dialect = netaddr.mac_unix_expanded
       return str(item)

    def _decode(self,item):
       return netaddr.EUI(item, dialect=netaddr.mac_unix_expanded)

class TimestampConverter(Converter):
    def encode(self,item):
       return item.strftime('%Y-%m-%d %H:%M:%S')

    def decode(self,item):
       return datetime.datetime.strptime(item or '1970-01-01 00:00:00','%Y-%m-%d %H:%M:%S')
