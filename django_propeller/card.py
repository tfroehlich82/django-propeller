# -*- coding: utf-8 -*-
from django_propeller.enums import CardItemTypes


class CardTitle(object):
    type = CardItemTypes.title
    text = ""
    size = 3


class CardSubtitle(object):
    type = CardItemTypes.subtitle
    text = ""


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
    header = None
    body = None
    style_inverse = True
    width = 4
