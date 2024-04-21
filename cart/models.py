from django.db import models
from shop.models import Product
from django.contrib.auth.models import User


class Delivery(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    free_shipping = models.BooleanField(default=False)
    free_shipping_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    payment_method = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        amount = sum(item.get_cost() for item in self.items.all())
        shipping = self.delivery.cost if not self.delivery.free_shipping or amount < self.delivery.free_shipping_amount else 0
        return amount + shipping


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

