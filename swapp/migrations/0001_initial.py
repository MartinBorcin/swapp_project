from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_groups(apps, schema_monitor):
    Group = apps.get_model("auth", "Group")
    Group.objects.bulk_create([
        Group(name='Staff'),
        Group(name='Seller'),
    ])


def remove_groups(apps, schema_monitor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Staff', 'Seller']).delete()


def create_initial_staff(apps, schema_monitor):
    User = apps.get_model('auth', 'User')
    user = User.objects.create(
        username='admin',
        password=make_password('admin'),
        email='',
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )
    Group = apps.get_model('auth', 'Group')
    staff_group = Group.objects.get(name='Staff')
    seller_group = Group.objects.get(name='Seller')
    user.groups.add(staff_group)
    user.groups.add(seller_group)
    user.save()


def remove_initial_staff(apps, schema_monitor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
        migrations.RunPython(create_initial_staff, remove_initial_staff)
    ]
