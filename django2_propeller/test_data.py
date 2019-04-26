# -*- coding: utf-8 -*-

"""Provides test data for unit tests"""


from .card import Card, CardActions, CardBody, CardHeader, CardMediaImage, CardMediaActions, CardSubtitle, CardTitle, \
    CardMedia
from .components import Button, FAB, Image
from .navbar import NavBar, NavBarLinkItem, NavBarDropDownItem, NavBarDropDownDivider


class DemoTitle1(CardTitle):
    text = "Title goes here"
    size = 2


class DemoHeaderTitle1(CardTitle):
    text = "Two-line item"
    size = 3


class DemoSubtitle1(CardSubtitle):
    text = "Secondary text"


class DemoMediaImage1(CardMediaImage):
    image = Image(source="http://propeller.in/assets/images/profile-pic.png", responsive=True)


class DemoMediaImage2(CardMediaImage):
    image = Image(source="http://propeller.in/assets/images/profile-pic.png", width=80, height=80)


class DemoMediaImage3(CardMediaImage):
    pass


class DemoMedia1(CardMedia):
    content = []


class DemoMedia2(CardMedia):
    content = [DemoMediaImage1(), ]


class DemoMedia3(CardMedia):
    content = [DemoTitle1, DemoSubtitle1, DemoMediaImage2(), ]
    style_inline = True


class DemoMedia4(CardMedia):
    content = None


class DemoMedia5(DemoMedia4):
    style_inline = True


class DemoBody1(CardBody):
    text = "Cards provide context and an entry point to more robust information and views. " \
           "Don't overload cards with extraneous information or actions."


class DemoHeader1(CardHeader):
    content_middle = [DemoHeaderTitle1(), DemoSubtitle1()]
    content_left = [Image("http://propeller.in/assets/images/avatar-icon-40x40.png", width=40, height=40, avatar=True)]


class DemoActions1(CardActions):
    items = [
        Button(content='primary', button_class='btn-primary'),
        Button('Action'),
        Button('third')
    ]


class DemoMediaActions1(CardMediaActions):
    items = [
        FAB('', button_class='btn-primary', icon='share', style='flat', size='sm'),
        FAB('', button_class='btn-primary', icon='thumb_up', style='flat', size='sm'),
        FAB('', button_class='btn-primary', icon='drafts', style='flat', size='sm')
    ]


class DemoCard1(Card):
    primary_title = DemoTitle1()
    secondary_title = DemoSubtitle1()
    header = DemoHeader1()
    actions = DemoActions1()
    media_actions = DemoMediaActions1()
    media = DemoMediaImage1()
    body = DemoBody1()


class DemoCard2(DemoCard1):
    body = None
    header = None
    actions = None


class DemoCard3(DemoCard1):
    style_inverse = True


class DemoCard4(DemoCard1):
    style_inline = True
    body = None
    header = None
    media_actions = None
    media = DemoMediaImage2()


class DemoCard5(DemoCard4):
    media = DemoMedia3()


class TestNavbar1(NavBar):
    brandname = 'propeller-test'
    brandurl = 'https://github.com/tfroehlich82/django-propeller'
    items = [
        NavBarLinkItem('Test1'),
        NavBarDropDownItem('Test2', items=[
            NavBarLinkItem('Test3'),
            NavBarLinkItem('Test4'),
            NavBarDropDownDivider(),
            NavBarLinkItem('Test5'),
        ]),
    ]


class TestNavbar2(TestNavbar1):
    style_inverse = True
    style_static = False
    brandurl = None


class TestNavbar3(TestNavbar1):
    style_inverse = False
    style_static = False


class TestNavbar4(TestNavbar1):
    brandurl = 'test'
    items = [
        NavBarLinkItem('Test1', url='http://example.org'),
        NavBarDropDownItem('Test2', items=[
            NavBarLinkItem('Test3', url='test'),
            NavBarLinkItem('Test4'),
            NavBarDropDownDivider(),
            NavBarLinkItem('Test5'),
        ]),
    ]

