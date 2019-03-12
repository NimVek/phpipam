#!/usr/bin/env python3

import abc

import logging
__log__ = logging.getLogger(__name__)


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
