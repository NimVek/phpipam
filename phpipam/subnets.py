#!/usr/bin/env python3

import netaddr

from . import generic
from . import converter

import logging
__log__ = logging.getLogger(__name__)


class Subnet(generic.CustomItem):
    _attributes = {
        'subnet': ('subnet', converter.IPConverter(), True),
        'mask': ('mask', converter.IntegerConverter(), True),
        'description': ('description', converter.StringConverter(), False),
        'section_id': ('sectionId', converter.IntegerConverter(), True),
        'ping': ('pingSubnet', converter.BooleanConverter(False), True),
        'discover': ('discoverSubnet', converter.BooleanConverter(False),
                     True),
    }

    @property
    def slaves(self):
        return [
            self.controller[x]
            for x in self.controller.get(self.id, 'slaves') or []
        ]

    @property
    def addresses(self):
        return [
            self.controller.api.addresses[x]
            for x in self.controller.get(self.id, 'addresses') or []
        ]

    @property
    def network(self):
        return netaddr.IPNetwork('%s/%d' % (self.subnet, self.mask))


class SubnetsController(generic.CustomController):
    def __init__(self, api, name='subnets'):
        super().__init__(api, name, Subnet)

    def cidr(self, addr):
        return [self.type(self, x) for x in self.get("cidr", str(addr)) or []]
