# Generated by Django 3.1.5 on 2021-11-16 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rentbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rtitle', models.CharField(max_length=200)),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True)),
                ('rimage', models.ImageField(blank=True, upload_to='products/%Y/%m/%d')),
                ('rpublisher', models.CharField(max_length=200)),
                ('rauthor', models.CharField(max_length=200)),
                ('rtotal', models.IntegerField()),
                ('rstock', models.IntegerField()),
                ('available_display', models.BooleanField(default=True, verbose_name='Display')),
                ('available_order', models.BooleanField(default=True, verbose_name='Order')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Rentcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('meta_description', models.TextField(blank=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=200)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply', models.DateTimeField(auto_now_add=True)),
                ('exp', models.DateField()),
                ('cust_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='??????')),
                ('rbook_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental.rentbook', verbose_name='????????????')),
            ],
            options={
                'ordering': ['-apply'],
            },
        ),
        migrations.AddField(
            model_name='rentbook',
            name='rcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='rental.rentcategory'),
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=500)),
                ('rent_date', models.DateField()),
                ('due', models.DateField()),
                ('rental_state', models.CharField(default='?????????', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cust_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='??????')),
                ('rbook_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental.rentbook', verbose_name='????????????')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AlterIndexTogether(
            name='rentbook',
            index_together={('id', 'slug')},
        ),
    ]
