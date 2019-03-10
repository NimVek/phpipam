#!/usr/bin/env python

from .api import API
from . import sections
from . import subnets
from . import addresses

import logging
__log__ = logging.getLogger(__name__)

API.controller['sections'] = sections.SectionsController
API.controller['subnets'] = subnets.SubnetsController
API.controller['addresses'] = addresses.AddressesController
