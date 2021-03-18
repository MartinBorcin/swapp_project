from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class User(models.Model):
#     # This line is required. Links User to a User model instance.
#     User = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.User.Username


class Item(models.Model):
    # foreign key
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    NAME_MAX_LENGTH = 50
    DESCRIPTION_MAX_LENGTH = 250
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    # django "id" - automatically assigned - no need for them in models
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)
    # defaults to False
    sold = models.BooleanField()
    checked = models.BooleanField()
    picture = models.ImageField(upload_to='item_pictures', blank=True)

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    # foreign key
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    # django "id" - automatically assigned - no need for them in models
    NAME_MAX_LENGTH = 50
    LOCATION_MAX_LENGTH = 100
    DESCRIPTION_MAX_LENGTH = 250
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    location = models.CharField(max_length=LOCATION_MAX_LENGTH)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    registration_start_time = models.DateTimeField()
    registration_end_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Checkout(models.Model):
    # foreign key
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # django "id" - automatically assigned - no need for them in models
    timestamp = models.DateTimeField()
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    paid = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    change = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        super(Checkout, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Announcement(models.Model):
    # foreign key
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # django "id" - automatically assigned - no need for them in models
    timestamp = models.DateTimeField()
    TITLE_MAX_LENGTH = 50
    DESCRIPTION_MAX_LENGTH = 250
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    picture = models.ImageField(upload_to='announcements', blank=True)

    def save(self, *args, **kwargs):
        super(Announcement, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

# hello
