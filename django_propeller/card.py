# -*- coding: utf-8 -*-
from django_propeller.enums import CardItemTypes

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class CardPrimaryTitle(object):
    text = ""


class CardSecondaryTitle(object):
    text = ""


class CardTitleIcon(object):
    url = None


class CardHeader(object):
    type = CardItemTypes.header
    content = []


class CardMedia(object):
    type = CardItemTypes.media
    content = []


class CardMediaActions(object):
    type = CardItemTypes.media_actions
    items = []


class CardActions(object):
    type = CardItemTypes.actions
    items = []


class CardBody(object):
    type = CardItemTypes.body
    content = ""


class Card(object):
    """Card is a class that generates a Propeller Card"""
    items = []
    style_inverse = True
