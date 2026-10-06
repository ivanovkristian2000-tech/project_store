from django.db import models
from apps.base.models import UUIDModel


class SupplierModel(UUIDModel):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'Supplier: {self.name}'

    class Meta:
        db_table = 'store_suppliers'
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['id']