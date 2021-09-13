from django.db import models
from django.urls import reverse
# Create your models here.
from accounts.models import User


class Rentcategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    meta_description = models.TextField(blank=True)

    slug = models.SlugField(max_length=200, db_index=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rental:rentbook_in_category', args=[self.slug])

class Rentbook(models.Model): #대여책 목록
    category = models.ForeignKey(Rentcategory, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    publisher = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    total = models.IntegerField()
    stock = models.IntegerField()
    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rental:rentbook_detail', args=[self.id, self.slug])
    #
    # def get_absolute_url(self):
    #     return reverse('rental:reserve', args=[self.id, self.slug])

class Rental(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    bookid = models.IntegerField()
    title = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    rentdate = models.DateField()
    expdate = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

class Reservation(models.Model):
    custnum = models.ForeignKey('accounts.User', verbose_name="회원", on_delete=models.CASCADE)
    bookid = models.ForeignKey('rental.Rentbook', verbose_name="대여도서", on_delete=models.CASCADE)
    applydate = models.DateTimeField(auto_now_add=True)
    exrent = models.DateField()

    class Meta:
        ordering = ['-applydate']

    def __str__(self):
        return str(self.custnum) + ' ' + str(self.bookid)

    def get_absolute_url(self):
        return reverse('rental:rentbook_detail', args=[self.bookid])
