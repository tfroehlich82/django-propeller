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


class CardMediaActions(object):
    type = CardItemTypes.media_actions.name
    items = []


class CardActions(object):
    type = CardItemTypes.actions.name
    items = []

    def __call__(self, *args, **kwargs):
        return self.items


class CardMedia(object):
    type = CardItemTypes.media.name
    orientation = 'default'
    content = None


class Card(object):
    """Card is a class that generates a Propeller Card"""
    primary_title = None
    secondary_title = None
    header = None
    media = None
    body = None
    actions = None
    media_actions = None
    style_inverse = False
    style_inline = False
    width = 4
