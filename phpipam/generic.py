#!/usr/bin/env python3

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
        return self.__class__.attributes

    @property
    def id(self):
        return int(self.values['id'])

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
            key, decoder = self.attributes[name]
            return decoder.decode(self.get(key))
        else:
            raise AttributeError

    def __setattr__(self, name, value):
        if name in self.attributes:
            key, encoder = self.attributes[name]
        else:
            raise AttributeError


class Controller(object):
    def __init__(self, api, name, typ):
        self.__api = api
        self.__name = name
        self.__type = typ

    @property
    def api(self):
        return self.__api

    @property
    def name(self):
        return self.__name

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
        return self.type(key)
