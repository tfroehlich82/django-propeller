# -*- coding: utf-8 -*-
try:
    from enum import Enum
except ImportError:
    from enum34 import Enum


class NavbarItemTypes(Enum):
    link = 1
    dropdown = 2
    divider = 3


class CardItemTypes(Enum):
    header = 1
    media = 2
    media_actions = 3
    actions = 4
