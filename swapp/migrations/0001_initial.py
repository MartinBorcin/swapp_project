# Generated by Django 2.2.17 on 2021-04-01 11:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('change', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('sold_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('sold', models.BooleanField(default=False)),
                ('checked', models.BooleanField(default=False)),
                ('picture', models.ImageField(blank=True, upload_to='item_pictures')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sold_in', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='swapp.Checkout')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('start_time', models.DateTimeField(default=datetime.datetime(2021, 4, 1, 11, 16, 19, 18215, tzinfo=utc))),
                ('end_time', models.DateTimeField(default=datetime.datetime(2021, 4, 1, 11, 16, 19, 18215, tzinfo=utc))),
                ('registration_start_time', models.DateTimeField(default=datetime.datetime(2021, 4, 1, 11, 16, 19, 18215, tzinfo=utc))),
                ('registration_end_time', models.DateTimeField(default=datetime.datetime(2021, 4, 1, 11, 16, 19, 18215, tzinfo=utc))),
                ('seller_cap', models.PositiveIntegerField(default=200)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2021, 4, 1, 11, 16, 19, 18215, tzinfo=utc))),
                ('title', models.CharField(max_length=50)),
                ('announcement', models.CharField(max_length=250)),
                ('picture', models.ImageField(blank=True, upload_to='announcements')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
