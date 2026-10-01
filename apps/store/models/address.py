from django.db import models


class AddressModel(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.street}, {self.house}'

    class Meta:
        verbose_name_plural = 'addresses'
