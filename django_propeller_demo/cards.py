from django_propeller.card import Card, CardHeader, CardMedia, CardActions, CardMediaActions


class DemoCard1(Card):
    primary_title = "Title goes here"
    secondary_title = "Secondary text"
    body = "Cards provide context and an entry point to more robust information and views. " \
           "Don't overload cards with extraneous information or actions."
