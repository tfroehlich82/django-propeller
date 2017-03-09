from django_propeller.card import Card, CardHeader, CardActions, CardMediaActions, CardTitle, CardSubtitle
from django_propeller.components import Image, Button, FAB


class DemoTitle1(CardTitle):
    text = "Title goes here"
    size = 2


class DemoSubtitle1(CardSubtitle):
    text = "Secondary text"


class DemoHeader1(CardHeader):
    content_middle = []


class DemoActions1(CardActions):
    items = [
        Button('primary', button_class='btn-primary'),
        Button('Action'),
        Button('third')
    ]


class DemoMediaActions1(CardMediaActions):
    items = [
        FAB('', button_class='btn-primary', icon='share', style='flat'),
        FAB('', button_class='btn-primary', icon='thumb_up', style='flat'),
        FAB('', button_class='btn-primary', icon='drafts', style='flat')
    ]


class DemoCard1(Card):
    primary_title = DemoTitle1
    secondary_title = DemoSubtitle1
    header = DemoHeader1
    actions = DemoActions1
    media_actions = DemoMediaActions1
    media = Image(source="http://propeller.in/assets/images/profile-pic.png", responsive=True).as_html()
    body = "Cards provide context and an entry point to more robust information and views. " \
           "Don't overload cards with extraneous information or actions."


class DemoCard2(DemoCard1):
    body = None
    header = None
    actions = None


class DemoCard3(DemoCard1):
    style_inverse = True

