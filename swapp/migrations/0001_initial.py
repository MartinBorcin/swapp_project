# Generated by Django 2.2.17 on 2021-03-17 16:19

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
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_seller', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('description', models.CharField(max_length=250)),
                ('sold', models.BooleanField(default=True)),
                ('checked', models.BooleanField(default=True)),
                ('picture', models.ImageField(blank=True, upload_to='item_images')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swapp.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('registration_start_time', models.DateTimeField()),
                ('registration_end_time', models.DateTimeField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swapp.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('change', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('sold_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swapp.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swapp.UserProfile')),
            ],
        ),
    ]
