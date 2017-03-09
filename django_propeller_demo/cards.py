from django_propeller.card import Card, CardHeader, CardActions, CardMediaActions, CardTitle, CardSubtitle
from django_propeller.components import Image, Button


class DemoTitle1(CardTitle):
    text = "Title goes here"
    size = 2


class DemoSubtitle1(CardSubtitle):
    text = "Secondary text"


class DemoHeader1(CardHeader):
    content_middle = []


class DemoActions1(CardActions):
    items = [
        Button('primary'),
        Button('Action'),
        Button('third')
    ]


class DemoMediaActions1(CardMediaActions):
    items = [
        Button('bla')
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
