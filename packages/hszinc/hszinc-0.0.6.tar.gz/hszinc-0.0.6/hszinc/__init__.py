# -*- coding: utf-8 -*-
# Zinc dumping and parsing module
# (C) 2016 VRT Systems
#
# vim: set ts=4 sts=4 et tw=78 sw=4 si:

from .grid import Grid
from .dumper import dump, dump_scalar
from .parser import parse, MODE_JSON, MODE_ZINC
from .metadata import MetadataObject
from .datatypes import Quantity, Coordinate, Uri, Bin, MARKER, REMOVE, Ref

__all__ = ['Grid', 'dump', 'parse', 'MetadataObject', 'Quantity',
        'Coordinate', 'Uri', 'Bin', 'MARKER', 'REMOVE', 'Ref',
        'MODE_JSON', 'MODE_ZINC']

__author__ = 'VRT Systems'
__copyright__ = 'Copyright 2016, VRT Systems'
__credits__ = ['VRT Systems']
__license__ = 'BSD'
__version__ = '0.0.6'
__maintainer__ = 'VRT Systems'
__email__ = 'support@vrt.com.au'
