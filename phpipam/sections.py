#!/usr/bin/env python3

from . import generic

import logging
__log__ = logging.getLogger(__name__)


class Section(generic.Item):
    attributes = {}

    @property
    def subnets(self):
        return [
            self.controller.api.subnets[x]
            for x in self.controller.get(self.id, 'subnets') or []
        ]


class SectionsController(generic.Controller):
    def __init__(self, api, name='sections'):
        super().__init__(api, name, Section)

    def __iter__(self):
        for x in self.get() or []:
            yield self.type(self,x)
