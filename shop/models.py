from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True)
    phone = models.CharField(max_length=200, db_index=True, default='+79000000000')
    email = models.CharField(max_length=200, db_index=True, default='example@example.com')

    def __str__(self):
        return f'{self.user.username} Profile'


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories', blank=True)
    primary = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    sorting_index = models.IntegerField(default=0)
    bought = models.PositiveIntegerField(default=0)
    limited = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    producer = models.TextField(default="Nvidia")
    reviews_num = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


class Reviews(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Озывы'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:reviews',
                       args=[self.product])
