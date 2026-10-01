from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from apps.store.models import CategoryModel, SupplierModel
from apps.base.models import UUIDModel


class ProductModel(UUIDModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, related_name='products')
    supplier = models.ForeignKey(SupplierModel, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    quantity = models.PositiveIntegerField(null=True, blank=True)
    article = models.CharField(max_length=100, unique=True, help_text="Unique string product id", db_index=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'Product: {self.name}'

    class Meta:
        db_table = 'store_products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['category', 'quantity']


class ProductDetailModel(UUIDModel):
    product = models.OneToOneField(ProductModel, on_delete=models.CASCADE, related_name='details')
    description = models.TextField(null=True, blank=True)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                 validators=[MinValueValidator(Decimal('0.0'))],
                                 help_text="Значение веса занимает не более 5 знаков до запятой!")

    def __str__(self):
        return f'Details of {self.product.name}'
