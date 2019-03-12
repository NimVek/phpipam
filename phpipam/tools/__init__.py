#!/usr/bin/env python3

from .. import interface
from . import tags

import logging
__log__ = logging.getLogger(__name__)

class ToolsController(interface.ControllerInterface,interface.APIInterface):
    controller = {}

    def execute(self,method,controller,identifiers,parameters):
       return self.api.execute(method, self.name,(controller,*identifiers), parameters)

ToolsController.controller['tags'] = tags.TagsController