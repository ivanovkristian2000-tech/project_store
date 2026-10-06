from django.db import models
from apps.base.models import UUIDModel

class AddressModel(UUIDModel):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=6)

    def __str__(self):
        return f'Address of customer: Street: {self.street}, House: {self.house}'

    class Meta:
        db_table = 'store_addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ('id',)




