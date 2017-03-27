======
Navbar
======


NavBarLinkItem
~~~~~~~~~~~~~~

.. autoclass:: django_propeller.navbar.NavBarLinkItem


NavBarDropDownDivider
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: django_propeller.navbar.NavBarDropDownDivider


NavBarDropDownItem
~~~~~~~~~~~~~~~~~~

.. autoclass:: django_propeller.navbar.NavBarDropDownItem


NavBar
~~~~~~

.. autoclass:: django_propeller.navbar.NavBar


NavBar Example
~~~~~~~~~~~~~~

navbar.py::

    from django_propeller.navbar import NavBar, NavBarLinkItem, NavBarDropDownItem, NavBarDropDownDivider

    class DemoNavBar(NavBar):
        brandname = "Brand"
        brandurl = "http://example.org"
        items = [
            NavBarLinkItem("Link"),
            NavBarDropDownItem("DropDown", [
                NavBarLinkItem("Action"),
                NavBarLinkItem("Another action"),
                NavBarDropDownDivider(),
                NavBarLinkItem("Separated link"),
                NavBarDropDownDivider(),
                NavBarLinkItem("One more separated link"),
            ])

        ]


your_view.py::

    from django.views.generic.base import TemplateView
    from django_propeller.views import NavBarMixin
    from your_project.navbar import DemoNavBar

    class HomePageView(TemplateView, NavBarMixin):
        template_name = 'your_template.html'
        navbar_class = DemoNavBar


your_template.html::

    {% load propeller %}
    {% propeller_navbar navbar %}
