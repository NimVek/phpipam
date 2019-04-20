#!/usr/bin/env python3

from . import interface
from . import converter

import logging
__log__ = logging.getLogger(__name__)


class Item(interface.ItemInterface):
    @property
    def attributes(self):
        result = {
            'id': ('id', converter.IntegerConverter(), True),
            'edit_date': ('editDate', converter.TimestampConverter(), True)
        }
        result.update(self.__class__._attributes)
        return result


class Custom(interface.ItemInterface):
    @property
    def attributes(self):
        return self.controller.custom_fields


class CustomItem(Item):
    @property
    def custom(self):
        return Custom(self.controller, self.values)


class Controller(interface.ControllerInterface):
    def __init__(self, api, name, typ):
        super().__init__(api, name)
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
        return self.type(self, key)


class CustomController(Controller):
    @property
    def custom_fields(self):
        result = {}
        for key, value in self.get("custom_fields").items():
            conv = converter.StringConverter()
            if value['type'] == 'text':
                conv = converter.StringConverter()
            elif value['type'] == 'tinyint(1)':
                conv = converter.BooleanConverter()
            result[key[7:]] = (key, conv, False)
        return result
