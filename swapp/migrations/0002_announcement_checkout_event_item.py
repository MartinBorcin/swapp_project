import datetime
from django.utils import timezone
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_initial_event(apps, schema_monitor):
    Event = apps.get_model('swapp', 'Event')
    User = apps.get_model('auth', 'User')
    user = User.objects.get(username='admin')
    now = datetime.datetime.now(datetime.timezone.utc)
    Event.objects.create(
        name='Event',
        creator=user,
        registration_start_time=now,
        registration_end_time=now,
        start_time=now,
        end_time=now,
        description='This an initial sample event to demonstrate the initial behaviour of the app.',
        location='5 Sample Street, Sometown',
    )


def remove_initial_event(apps, schema_monitor):
    Event = apps.get_model('swapp', 'Event')
    Event.objects.get(name='Event').delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('swapp', '0001_initial'),
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
                ('description', models.CharField(max_length=250, blank=True)),
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
                ('start_time', models.DateTimeField(default=timezone.now)),
                ('end_time', models.DateTimeField(default=timezone.now)),
                ('registration_start_time', models.DateTimeField(default=timezone.now)),
                ('registration_end_time', models.DateTimeField(default=timezone.now)),
                ('seller_cap', models.PositiveIntegerField(default=200)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=timezone.now)),
                ('title', models.CharField(max_length=50)),
                ('announcement', models.CharField(max_length=250)),
                ('picture', models.ImageField(blank=True, upload_to='announcements')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_initial_event, remove_initial_event),
    ]
