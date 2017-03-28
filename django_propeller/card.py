# -*- coding: utf-8 -*-

"""This module contains classes for constructing propeller cards"""

from django.utils.safestring import mark_safe

from .utils import render_tag, add_css_class
from .components import Button, FAB, Image
from .text import text_concat
from .exceptions import PropellerException


class CardTitle(object):

    """
    Renders a Card Title.

    **Parameters**:

        text
            The display text for the title.

        size
            The size for the title as integer. Works with the h-tag, so size=1 is bigger than size=3.
            Optional. (default=3)
    """

    text = ""
    size = 3

    def as_html(self):
        """Returns card title as html"""
        tag = 'h%d' % self.size
        attrs = {'class': 'pmd-card-title-text'}
        content = self.text
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardSubtitle(object):

    """
    Renders a Card Subtitle.

    **Parameters**:

        text
            The display text for the subtitle.
    """

    text = ""

    def as_html(self):
        """Returns card subtitle as html"""
        tag = 'span'
        attrs = {'class': 'pmd-card-subtitle-text'}
        content = self.text
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardBody(object):

    """
    Renders a Card Body.

    **Parameters**:

        text
            The text to display in the body.
    """

    text = ""

    def as_html(self):
        """Returns card body as html"""
        tag = 'div'
        attrs = {'class': 'pmd-card-body'}
        content = self.text
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardHeader(object):

    """
    Renders a Card Header.

    **Parameters**:

        content_left
            A list of items to display on the left of header. 
            May contain Button, FAB, Image, CardTitle, or CardSubtitle.

        content_middle
            A list of items to display in the middle of header. 
            May contain Button, FAB, Image, CardTitle, or CardSubtitle.
    """

    content_left = []
    content_middle = []

    def get_left_content(self):
        """Returns left content of card header as html"""
        tag = 'div'
        attrs = {'class': 'media-left'}
        content = ''
        for itm in self.content_left:
            content = text_concat(content, mark_safe(itm.as_html()))
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )

    def get_middle_content(self):
        """Returns middle content of card header as html"""
        tag = 'div'
        attrs = {'class': 'media-body media-middle'}
        content = ''
        for itm in self.content_middle:
            content = text_concat(content, mark_safe(itm.as_html()))
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )

    def as_html(self):
        """Returns card header as html"""
        tag = 'div'
        attrs = {'class': 'pmd-card-title'}
        content = text_concat(self.get_left_content(), self.get_middle_content())
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardMediaActions(object):

    """
    Renders Card Media Actions.

    **Parameters**:

        items
            A list of items to display in the Card Media Action section. 
            May contain Button or FAB.
    """

    items = []

    def as_html(self):
        """Returns card media actions as html"""
        tag = 'div'
        attrs = {'class': 'pmd-card-actions'}
        content = ''
        for btn in self.items:
            if isinstance(btn, FAB):
                content = text_concat(content, mark_safe(btn.as_html()))
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardActions(object):

    """
    Renders Card Actions.

    **Parameters**:

        items
            A list of items to display in the Card Action section. 
            May contain Button or FAB.
    """

    items = []

    def as_html(self):
        """Returns card actions as html"""
        tag = 'div'
        attrs = {'class': 'pmd-card-actions'}
        content = ''
        for btn in self.items:
            if isinstance(btn, Button):
                content = text_concat(content, mark_safe(btn.as_html()))
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardMediaImage(object):

    """
    Renders a Card Media Image.

    **Parameters**:

        image
            Must be an instance of an Image.
    """

    image = None

    def as_html(self):
        """Returns card media image as html"""
        if isinstance(self.image, Image):
            return self.image.as_html()
        return None


class CardMedia(object):

    """
    Renders Card Media

    **Parameters**:

        content
            if style_inline=True:
                A list of items to display in the card media section. 
                May contain CardMediaImage, CardTitle, or CardSubtitle.
            or if style_inline=False: (default)
                A instance of CardMediaImage

        style_inline
            Display card with inline style if true. (Default: False)
    """

    content = None
    style_inline = False

    def get_media_body_inline(self):
        """Returns media body inline as html"""
        tag = 'div'
        attrs = {'class': 'media-body'}
        content = ''
        if self.style_inline:
            if not isinstance(self.content, list):
                raise PropellerException("Propeller Card: content must be a list")
            for itm in self.content:
                if isinstance(itm, (CardTitle, CardSubtitle)):
                    content = text_concat(content, mark_safe(itm.as_html()))
            content = text_concat(content, mark_safe('</div>'))
            content = text_concat(content, mark_safe('<div class="media-right media-middle">'))
            for itm in self.content:
                if isinstance(itm, CardMediaImage):
                    content = text_concat(content, mark_safe(itm.as_html()))
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )

    def get_media_body(self):
        """Returns media body as html"""
        if self.style_inline:
            return self.get_media_body_inline()

        tag = 'div'
        attrs = {'class': 'media-body'}
        content = ''
        if not isinstance(self.content, list):
            raise PropellerException("Propeller Card: content must be a list")
        for itm in self.content:
            if isinstance(itm, CardMediaImage):
                content = text_concat(content, mark_safe(itm.as_html()))

        return render_tag(tag, attrs=attrs, content=mark_safe(content), )

    def as_html(self):
        """Returns card media as html"""
        tag = 'div'
        attrs = {'class': 'pmd-card-media'}
        content = self.get_media_body()
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class Card(object):

    """
    Card is a class that generates a Propeller Card.

    **Parameters**:

        primary_title
            An instance of CardTitle. Optional.

        secondary_title
            An instance of CardSubtitle. Optional.

        header
            An instance of CardHeader. Optional.

        media
            An instance of CardMedia. Optional.

        body
            An instance of CardBody. Optional.

        actions
            An instance of CardActions. Optional.

        media_actions
            An instance of CardMediaActions. Optional.

        style_inverse
            Display dark style if true. (Default: False)

        style_inline
            Display card with inline style if true. (Default: False)

        width
            Width of the card in Bootstrap grid (col-md) as integer. (Default: 4)
    """

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

    def get_actions(self):
        """Returns actions of card as html"""
        actions = ''
        if self.media_actions:
            actions = text_concat(actions, self.media_actions.as_html())
        if self.actions:
            actions = text_concat(actions, self.actions.as_html())
        return actions

    def get_content(self):
        """Returns content of card as html"""
        content = ''
        if self.header and not self.style_inline:
            content = text_concat(content, self.header.as_html())
        if self.media:
            content = text_concat(content, self.media.as_html())
        if not self.style_inline:
            if self.primary_title or self.secondary_title:
                content = text_concat(content, '<div class="pmd-card-title">')
                if self.primary_title:
                    content = text_concat(content, self.primary_title.as_html())
                if self.secondary_title:
                    content = text_concat(content, self.secondary_title.as_html())
                content = text_concat(content, '</div>')
            if self.body:
                content = text_concat(content, self.body.as_html())
        content = text_concat(content, self.get_actions())
        return content

    def as_html(self):
        """Returns card as html"""
        tag = 'div'
        classes = 'pmd-card'
        if self.style_inline:
            classes = add_css_class(classes, 'pmd-card-media-inline')
        if self.style_inverse:
            classes = add_css_class(classes, 'pmd-card-inverse')
        else:
            classes = add_css_class(classes, 'pmd-card-default')
        classes = add_css_class(classes, 'pmd-z-depth')
        classes = add_css_class(classes, 'col-md-%d' % self.width)
        attrs = {'class': classes}
        content = self.get_content()
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )
