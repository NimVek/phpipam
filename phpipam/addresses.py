#!/usr/bin/env python3

from . import generic
from . import converter

import logging
__log__ = logging.getLogger(__name__)


class Address(generic.Item):
    attributes = {
        'exclude_ping': ('excludePing', converter.BooleanConverter()),
        'subnet_id': ('subnetId', converter.IntegerConverter()),
        'ip': ('ip', converter.IPConverter())
    }

    @property
    def subnet(self):
        return self.controller.api.subnets[self.subnet_id]


class AddressesController(generic.Controller):
    def __init__(self, api, name='addresses'):
        super().__init__(api, name, Address)

    def search(self, addr):
        return [self.type(self,x) for x in self.get("search", str(addr)) or []]
