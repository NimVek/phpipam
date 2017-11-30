#!/usr/bin/env python

import generic

import logging
__log__ = logging.getLogger(__name__)


class Address(generic.Item):
    def get(self, name):
        if name == 'subnet':
            return self._controller.api.controller('subnets').get(
                self.get('subnetId'))
        else:
            return super(Address, self).get(name)


class AddressesController(generic.Controller):
    def __init__(self, api):
        super(AddressesController, self).__init__(api, "addresses")

    def search(self, addr):
        return [
            Address(self, x)
            for x in (self._execute("GET", ["search", addr]) or [])
        ]


generic.API.controller['addresses'] = AddressesController
