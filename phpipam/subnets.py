#!/usr/bin/env python

import generic

import logging
__log__ = logging.getLogger(__name__)


class SubnetsController(generic.Controller):
    def __init__(self, api):
        super(SubnetsController, self).__init__(api, "subnets")

    def cidr(self, addr):
        return [
            Item(self, x) for x in (self._execute("GET", ["cidr", addr]) or [])
        ]


generic.API.controller['subnets'] = SubnetsController
