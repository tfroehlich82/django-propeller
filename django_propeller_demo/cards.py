from django_propeller.card import Card, CardHeader, CardMedia, CardActions, CardMediaActions, CardTitle, CardSubtitle


class DemoTitle1(CardTitle):
    text = "Title goes here"
    size = 2


class DemoSubtitle1(CardSubtitle):
    text = "Secondary text"


class DemoHeader1(CardHeader):
    content_middle = []


class DemoCard1(Card):
    primary_title = DemoTitle1
    secondary_title = DemoSubtitle1
    header = DemoHeader1
    body = "Cards provide context and an entry point to more robust information and views. " \
           "Don't overload cards with extraneous information or actions."
