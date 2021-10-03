from django.db import models
from django.urls import reverse

# Create your models here.
class Buycategory(models.Model):
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
        return reverse('shop:buybook_in_category', args=[self.slug])


class Buybook(models.Model):
    bcategory = models.ForeignKey(Buycategory, on_delete=models.SET_NULL, null=True, related_name='products')
    btitle = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    bpublisher = models.CharField(max_length=200)
    bauthor = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bcontent = models.TextField()
    btotal = models.IntegerField()
    bstock = models.IntegerField()
    STATE={
        ('최상', '최상'),
        ('상', '상'),
        ('중', '중'),
        ('하', '하')
    }
    condition = models.CharField(max_length=10, choices=STATE, default="최상")

    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.btitle

    def get_absolute_url(self):
        return reverse('shop:buybook_detail', args=[self.id, self.slug])