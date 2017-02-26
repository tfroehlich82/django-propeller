from django_propeller.navbar import NavBar, NavBarLinkItem, NavBarDropDownItem, NavBarDropDownDivider


class MainNavBar(NavBar):
    brandname = "django-propeller"
    brandurl = "https://github.com/tfroehlich82/django-propeller"
    items = [
        NavBarLinkItem("Home", "home"),
        NavBarLinkItem("Typography", "typo"),
        NavBarLinkItem("Buttons", "buttons"),
        NavBarLinkItem("Floating Action Buttons", "fabs"),
        NavBarLinkItem("Navbar", "navbar"),
        NavBarDropDownItem("Forms", [
            NavBarLinkItem("Form", "form_default"),
            NavBarLinkItem("Formset", "formset_default"),
            NavBarLinkItem("Form by field", "form_by_field"),
            NavBarLinkItem("Form horizontal", "form_horizontal"),
            NavBarLinkItem("Form inline", "form_inline"),
            NavBarLinkItem("Form with files", "form_with_files"),
        ]),
        NavBarLinkItem("Pagination", "pagination"),
        NavBarLinkItem("Miscellaneous", "misc"),
    ]


class DemoNavBar1(NavBar):
    brandname = "Brand"
    items = [
        NavBarLinkItem("Link"),
        NavBarLinkItem("Link"),
        NavBarDropDownItem("DropDown", [
            NavBarLinkItem("Link"),
            NavBarLinkItem("Link"),
            NavBarDropDownDivider(),
            NavBarLinkItem("Link"),
        ])

    ]
