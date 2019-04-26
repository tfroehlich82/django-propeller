====
Card
====


CardTitle
~~~~~~~~~

.. autoclass:: django2_propeller.card.CardTitle


CardSubtitle
~~~~~~~~~~~~

.. autoclass:: django2_propeller.card.CardSubtitle


CardBody
~~~~~~~~

.. autoclass:: django2_propeller.card.CardBody


CardHeader
~~~~~~~~~~

.. autoclass:: django2_propeller.card.CardHeader


CardMediaActions
~~~~~~~~~~~~~~~~

.. autoclass:: django2_propeller.card.CardMediaActions


CardActions
~~~~~~~~~~~

.. autoclass:: django2_propeller.card.CardActions


CardMediaImage
~~~~~~~~~~~~~~

.. autoclass:: django2_propeller.card.CardMediaImage


CardMedia
~~~~~~~~~

.. autoclass:: django2_propeller.card.CardMedia


Card
~~~~

.. autoclass:: django2_propeller.card.Card


Card Example
~~~~~~~~~~~~

card.py::

    from django2_propeller.card import Card, CardHeader, CardActions, CardMediaActions, CardTitle, CardSubtitle, \
    CardMediaImage, CardBody, CardMedia
    from django2_propeller.components import Image, Button, FAB

    class DemoTitle(CardTitle):
        text = "Title goes here"
        size = 2


    class DemoSubtitle(CardSubtitle):
        text = "Secondary text"


    class DemoMediaImage(CardMediaImage):
        image = Image(source="http://propeller.in/assets/images/profile-pic.png", responsive=True)


    class DemoMedia(CardMedia):
        content = [DemoMediaImage(), ]


    class DemoBody(CardBody):
        text = "Cards provide context and an entry point to more robust information and views. " \
               "Don't overload cards with extraneous information or actions."


    class DemoHeader(CardHeader):
        content_middle = [DemoTitle(), DemoSubtitle()]


    class DemoActions(CardActions):
        items = [
            Button(content='primary', button_class='btn-primary'),
            Button('Action'),
        ]


    class DemoMediaActions(CardMediaActions):
        items = [
            FAB('', button_class='btn-primary', icon='share', style='flat', size='sm'),
            FAB('', button_class='btn-primary', icon='thumb_up', style='flat', size='sm'),
            FAB('', button_class='btn-primary', icon='drafts', style='flat', size='sm')
        ]


    class DemoCard(Card):
        primary_title = DemoTitle()
        secondary_title = DemoSubtitle()
        header = DemoHeader()
        actions = DemoActions()
        media_actions = DemoMediaActions()
        media = DemoMedia()
        body = DemoBody()


your_template.html::

    {% load propeller %}
    {% propeller_card card %}
