# -*- coding: utf-8 -*-
from django.db import models


class NavbarItem(models.Model):
    url = models.URLField()
    text = models.CharField(max_length=80)


class Navbar(models.Model):
    brand = models.CharField(max_length=200)
    items = models.ForeignKey(NavbarItem, on_delete=models.CASCADE)
