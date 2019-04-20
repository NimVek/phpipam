#!/usr/bin/env python3

import abc

import logging
__log__ = logging.getLogger(__name__)


class ItemInterface(abc.ABC):
    def __init__(self, controller, item):
        self.__controller = controller
        self.__refresh(item)

    @property
    def controller(self):
        return self.__controller

    @property
    def values(self):
        return self.__values

    def __refresh(self, item):
        if isinstance(item, (int, str)):
            self.__values = self.controller.get(item)
        elif isinstance(item, dict):
            self.__values = item
        else:
            raise TypeError

    def refresh(self):
        self.__refresh(self.values['id'])

    @property
    @abc.abstractmethod
    def attributes(self):
        raise NotImplementedError

    def get(self, name):
        return self.values[name]

    def set(self, name, value):
        if self.values[name] != value:
            if self.controller.patch(
                    self.values['id'], id=self.values['id'], **{name: value}):
                self.values[name] = value
                return True
        return False

    def __getattr__(self, name):
        if name in self.attributes:
            key, decoder, _ = self.attributes[name]
            return decoder.decode(self.get(key))
        else:
            __log__.debug((name))
            raise AttributeError("'%s' object has no attribute '%s'" %
                                 (self.__class__.__name__, name))

    def __setattr__(self, name, value):
        obj = getattr(self.__class__, name, None)
        if isinstance(obj, property):
            if not obj.fset:
                raise AttributeError("can't set attribute")
            else:
                obj.fset(self, value)
        elif name.startswith('_ItemInterface__'):
            super().__setattr__(name, value)
        elif name in self.attributes:
            key, encoder, read_only = self.attributes[name]
            if read_only:
                raise AttributeError("can't set attribute")
            else:
                self.set(key, encoder.encode(value))
        else:
            raise AttributeError("'%s' object has no attribute '%s'" %
                                 (self.__class__.__name__, name))


class APIInterface(abc.ABC):
    @abc.abstractmethod
    def execute(self, method, controller, indentifiers, parameters):
        raise NotImplementedError

    def __getattr__(self, name):
        if name in self.controller:
            tmp = self.controller[name](self, name)
            self.__setattr__(name, tmp)
            return tmp
        else:
            raise AttributeError("'%s' object has no attribute '%s'" %
                                 (self.__class__.__name__, name))


class ControllerInterface(abc.ABC):
    def __init__(self, api, name):
        self.__api = api
        self.__name = name

    @property
    def api(self):
        return self.__api

    @property
    def name(self):
        return self.__name
