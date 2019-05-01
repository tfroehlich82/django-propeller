from django2_propeller.navbar import NavBar, NavBarLinkItem, NavBarDropDownItem, NavBarDropDownDivider


class MainNavBar(NavBar):
    brandname = "django2-propeller"
    brandurl = "https://github.com/RaddishIoW/django2-propeller"
    items = [
        NavBarLinkItem("Home", "home"),
        NavBarLinkItem("Typography", "typo"),
        NavBarLinkItem("Cards", "cards"),
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
            NavBarLinkItem("Action"),
            NavBarLinkItem("Another action"),
            NavBarLinkItem("Something else here"),
            NavBarDropDownDivider(),
            NavBarLinkItem("Separated link"),
            NavBarDropDownDivider(),
            NavBarLinkItem("One more separated link"),
        ])

    ]


class DemoNavBar2(DemoNavBar1):
    style_inverse = False
