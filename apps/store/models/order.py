from django.db import models
from django.core.validators import MinValueValidator
from apps.store.models import CustomerModel, ProductModel
from apps.base.models import UUIDModel


class OrderModel(UUIDModel):
    order_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(CustomerModel, on_delete=models.PROTECT, related_name='orders')

    def __str__(self):
        return f'Order {self.id} by {self.customer}'

    class Meta:
        db_table = 'store_orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-order_date']
        get_latest_by = 'order_date'


class OrderItemModel(UUIDModel):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f'{self.quantity} x {self.product} for {self.order}'