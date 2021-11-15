from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from accounts.models import User
from rental.models import Rentbook


class Rent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    detailadd = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    # discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'Order {}'.format(self.id)


from shop.models import Buybook
class RentItem(models.Model):
    order = models.ForeignKey(Rent, on_delete=models.CASCADE, related_name = 'items')
    product = models.ForeignKey(Rentbook, on_delete=models.PROTECT, related_name='rent_products')
    rent_date = models.DateField()
    due = models.DateField()
    rental_state = models.CharField(max_length=10, default='대여중')
    created = models.DateTimeField(auto_now_add=True)
    cust = models.ForeignKey('accounts.User', verbose_name="회원", on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.id)

    def overdue(self):
        now = datetime.now().date()
        overdue = '연체'
        date = now > self.due
        if date == True and self.rental_state=='대여중':
            return overdue

import hashlib
from .iamport import payments_prepare, find_transaction
class RentTransactionManager(models.Manager):
    def create_new(self, order, amount, success=None, transaction_status=None):
        if not order:
            raise ValueError("주문 오류")

        order_hash = hashlib.sha1(str(order.id).encode('utf-8')).hexdigest()
        email_hash = str(order.email).split("@")[0]
        final_hash = hashlib.sha1((order_hash + email_hash).encode('utf-8')).hexdigest()[:10]
        merchant_order_id = "%s"%(final_hash)

        payments_prepare(merchant_order_id, amount)

        transaction = self.model(
            order=order,
            merchant_order_id = merchant_order_id,
            amount=amount
        )

        if success is not None:
            transaction.success = success
            transaction.transaction_status = transaction_status

        try:
            transaction.save()
        except Exception as e:
            print("save error", e)

        return transaction.merchant_order_id

    def get_transaction(self, merchant_order_id):
        result = find_transaction(merchant_order_id)
        if result['status'] == 'paid':
            return result
        else:
            return None


class RentTransaction(models.Model):
    order = models.ForeignKey(Rent, on_delete=models.CASCADE)
    merchant_order_id = models.CharField(max_length=120, null=True, blank=True)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)
    type = models.CharField(max_length=120, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = RentTransactionManager()

    def __str__(self):
        return str(self.order.id)

    class Meta:
        ordering = ['-created']


def order_payment_validation(sender, instance, created, *args, **kwargs):
    if instance.transaction_id:
        import_transaction = RentTransaction.objects.get_transaction(merchant_order_id=instance.merchant_order_id)

        merchant_order_id = import_transaction['merchant_order_id']
        imp_id = import_transaction['imp_id']
        amount = import_transaction['amount']

        local_transaction = RentTransaction.objects.filter(merchant_order_id=merchant_order_id, transaction_id = imp_id, amount=amount).exists()

        if not import_transaction or not local_transaction:
            raise ValueError("비정상 거래입니다.")

from django.db.models.signals import post_save
post_save.connect(order_payment_validation, sender=RentTransaction)