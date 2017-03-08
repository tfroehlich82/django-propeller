# -*- coding: utf-8 -*-
from django_propeller.enums import CardItemTypes

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class CardTitle(object):
    pass


class CardSubtitle(object):
    pass


class CardHeader(object):
    type = CardItemTypes.header.name
    content_left = []
    content_middle = []


class CardMedia(object):
    type = CardItemTypes.media.name
    content = []


class CardMediaActions(object):
    type = CardItemTypes.media_actions.name
    items = []


class CardActions(object):
    type = CardItemTypes.actions.name
    items = []


class Card(object):
    """Card is a class that generates a Propeller Card"""
    primary_title = None
    secondary_title = None
    title_icon = None
    body = None
    style_inverse = True
    width = 4
