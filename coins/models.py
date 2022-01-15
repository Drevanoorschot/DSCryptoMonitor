from django.db import models


# Create your models here.
class Coin(models.Model):
    name = models.CharField(max_length=50, unique=True)
    shorthand = models.CharField(max_length=10, unique=True)


class Exchange(models.Model):
    name = models.CharField(max_length=50, unique=True)
    website = models.URLField(unique=True)
    markets_page = models.URLField(unique=True)
    base_xpath = models.CharField(max_length=1000)


class ExceptionRule(models.Model):
    class ExceptionKind(models.TextChoices):
        NOT_TRADED = 'NTD',
        DIFF_COIN_SHORTHAND = 'DCS',
        DIFF_XPATH = 'DXP',

    forCoin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    forExchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    kind = models.CharField(max_length=3, choices=ExceptionKind.choices)
    value = models.CharField(max_length=1000)

    class Meta:
        unique_together = [['forCoin', 'forExchange', 'kind']]
