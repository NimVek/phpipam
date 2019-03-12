#!/usr/bin/env python3

from .. import generic
from .. import converter

import logging
__log__ = logging.getLogger(__name__)


class Tag(generic.Item):
    _attributes = {
        'type': ('type', converter.StringConverter(), False),
        'show': ('showtag', converter.BooleanConverter(False), False),
        #        'background': ('bgcolor', converter.ColorConverter(), False),
        #        'foreground': ('fgcolor', converter.ColorConverter(), False),
        'compress': ('compress', converter.YesNoConverter(False), False),
        'locked': ('locked', converter.YesNoConverter(False), True),
        'update': ('updateTag', converter.BooleanConverter(False), False),
    }


class TagsController(generic.Controller):
    def __init__(self, api, name='tags'):
        super().__init__(api, name, Tag)
