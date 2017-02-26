# -*- coding: utf-8 -*-
try:
    from enum import Enum
except ImportError:
    from enum34 import Enum


class NavbarItemTypes(Enum):
    link = 1
    dropdown = 2
