from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class DepositRequest(models.Model):

    date = models.DateField()
    periods = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(60)])
    amount = models.PositiveIntegerField(validators=[MinValueValidator(10000), MaxValueValidator(3000000)])
    rate = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    results = models.TextField()