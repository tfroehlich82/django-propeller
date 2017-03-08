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
    body = 1
    header = 2
    media = 3
    media_actions = 4
    actions = 5
