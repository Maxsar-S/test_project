from django.db import models
from django.contrib.auth.models import User
from test_project import settings


class Item(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    price = models.IntegerField()

    US_DOLLAR = 'USD'
    EURO = 'EUR'
    CURRENCY_CHOICES = [
        (US_DOLLAR, 'USD'),
        (EURO, 'EUR'),
    ]

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default=US_DOLLAR,
    )

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class Discount(models.Model):
    pass


class Tax(models.Model):
    pass
