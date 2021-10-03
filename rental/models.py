from datetime import datetime

from django.db import models
from django.urls import reverse
from datetime import timedelta, date
from django.utils import timezone
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
    rcategory = models.ForeignKey(Rentcategory, on_delete=models.SET_NULL, null=True, related_name='products')
    rtitle = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    rimage = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    rpublisher = models.CharField(max_length=200)
    rauthor = models.CharField(max_length=200)
    rtotal = models.IntegerField()
    rstock = models.IntegerField()

    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created']
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.rtitle

    def get_absolute_url(self):
        return reverse('rental:rentbook_detail', args=[self.id, self.slug])



class Rental(models.Model):
    # RENTAL_STATE = (
    #     ('대여', '대여'),
    #     ('반납예약', '반납예약'),
    #     ('반납완료', '반납완료')
    # )
    cust_num = models.ForeignKey('accounts.User', verbose_name="회원", on_delete=models.CASCADE)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    rbook_id = models.ForeignKey('rental.Rentbook', verbose_name="대여도서", on_delete=models.CASCADE)
    rent_date = models.DateField()
    due = models.DateField()
    rental_state = models.CharField(max_length=10, default='대여중')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.cust_num)

    def overdue(self):
        now = datetime.now().date()
        overdue = '연체'
        date = now > self.due
        if date == True and self.rental_state=='대여중':
            return overdue

    def get_absolute_url(self):
        return reverse('rental:rental_return', args=[self.id])


class Reservation(models.Model):
    cust_num = models.ForeignKey('accounts.User', verbose_name="회원", on_delete=models.CASCADE)
    rbook_id = models.ForeignKey('rental.Rentbook', verbose_name="대여도서", on_delete=models.CASCADE)
    apply = models.DateTimeField(auto_now_add=True)
    exp = models.DateField()

    class Meta:
        ordering = ['-apply']

    def __str__(self):
        return str(self.cust_num) + ' ' + str(self.rbook_id)

    def get_absolute_url(self):
        return reverse('rental:rentbook_detail', args=[self.rbook_id])