#!/usr/bin/env python3

from . import generic
from . import converter

import logging
__log__ = logging.getLogger(__name__)


class Address(generic.Item):
    _attributes = {
        'subnet_id': ('subnetId', converter.IntegerConverter(), True),
        'ip': ('ip', converter.IPConverter(), True),
        'is_gateway': ('is_gateway', converter.BooleanConverter(), False),
        'description': ('description', converter.StringConverter(), False),
        'hostname': ('hostname', converter.StringConverter(), False),
        'mac': ('mac', converter.MACConverter(), False),
        'owner': ('owner', converter.StringConverter(), False),
#        'tag': ('tag', converter.TagConverter(), False),
        'ptr_ignore': ('PTRignore', converter.BooleanConverter(), False),
        'ptr': ('PTR', converter.IntegerConverter(), False),
        'device_id': ('deviceId', converter.IntegerConverter(), False),
        'port': ('port', converter.StringConverter(), False),
        'note': ('note', converter.StringConverter(), False),
        'last_seen': ('lastSeen', converter.TimestampConverter(), False),
        'exclude_ping': ('excludePing', converter.BooleanConverter(), False),
    }

    @property
    def subnet(self):
        return self.controller.api.subnets[self.subnet_id]

    @property
    def tag(self):
        return self.controller.TagConverter.decode(self.get('tag'))

    @tag.setter
    def tag(self, value):
        self.set('tag',self.controller.TagConverter.encode(value))


class AddressesController(generic.Controller):
    def __init__(self, api, name='addresses'):
        super().__init__(api, name, Address)
        self.__tag_converter = None

    def search(self, addr):
        return [self.type(self,x) for x in self.get("search", str(addr)) or []]

    @property
    def TagConverter(self):
        if not self.__tag_converter:
         self.__tag_converter = converter.DictionaryConverter({ x['type']: x['id'] for x in self.get('tags') or []}, 'Offline')
        return self.__tag_converter
