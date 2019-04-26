from django2_propeller.card import Card, CardHeader, CardActions, CardMediaActions, CardTitle, CardSubtitle, \
    CardMediaImage, CardBody, CardMedia
from django2_propeller.components import Image, Button, FAB


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


class DemoMedia1(CardMedia):
    content = [DemoMediaImage1(), ]


class DemoMedia2(CardMedia):
    content = [DemoTitle1(), DemoSubtitle1(), DemoMediaImage2(), ]


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
    media = DemoMedia1()
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
    media = DemoMedia2()
