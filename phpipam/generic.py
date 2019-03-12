#!/usr/bin/env python3

from . import interface
from . import converter

import logging
__log__ = logging.getLogger(__name__)


class Item(object):
    def __init__(self, controller, item):
        self.__controller = controller
        if isinstance(item, int):
            self.__values = self.controller.get(item)
        elif isinstance(item, dict):
            self.__values = item
        else:
            raise TypeError

    @property
    def controller(self):
        return self.__controller

    @property
    def values(self):
        return self.__values

    @property
    def attributes(self):
        result = {
          'id': ('id', converter.IntegerConverter(), True),
          'edit_date': ('editDate', converter.TimestampConverter(), True)
        }
        result.update(self.__class__._attributes)
        return result

    def get(self, name):
        return self.values[name]

    def set(self, name, value):
        if self.values[name] != value:
            if self.controller.patch(self.id, id=self.id, **{name: value}):
                self.values[name] = value
                return True
        return False

    def __getattr__(self, name):
        if name in self.attributes:
            key, decoder, read_only = self.attributes[name]
            return decoder.decode(self.get(key))
        else:
            __log__.debug((name))
            raise AttributeError

    def __setattr__(self, name, value):
        if name in self.attributes:
            key, encoder, read_only = self.attributes[name]
            self.set(key,encoder.encode(value))
        elif name.startswith('_Item__'):
          super().__setattr__(name,value)
        else:
            raise AttributeError


class Controller(interface.ControllerInterface):
    def __init__(self, api, name, typ):
        super().__init__(api,name)
        self.__type = typ

    @property
    def type(self):
        return self.__type

    def execute(self, method, *identifiers, **parameters):
        return self.api.execute(method, self.name, identifiers, parameters)

    def get(self, *identifiers):
        return self.api.execute("GET", self.name, identifiers, {})

    def patch(self, *identifiers, **values):
        return self.api.execute("PATCH", self.name, identifiers, values)

    put = patch

    def __getitem__(self, key):
        return self.type(self,key)
