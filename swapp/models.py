from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# class User(models.Model):
#     # This line is required. Links User to a User model instance.
#     User = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.User.Username


class Checkout(models.Model):
    # foreign key
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # django "id" - automatically assigned - no need for them in models
    timestamp = models.DateTimeField()
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    paid = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    change = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Checkout, self).save(*args, **kwargs)

    def __str__(self):
        return f"<Checkout #{str(self.id)}, performed by: {self.sold_by.username} at {self.timestamp}>"


class Item(models.Model):
    # foreign key
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    sold_in = models.ForeignKey(Checkout, on_delete=models.CASCADE, null=True, blank=True)

    NAME_MAX_LENGTH = 50
    DESCRIPTION_MAX_LENGTH = 250
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    # django "id" - automatically assigned - no need for them in models
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH, blank=True)
    # defaults to False
    sold = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='item_pictures', blank=True)

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return f"Item #{str(self.id)}, offered by {self.seller.username}"


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

    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

    registration_start_time = models.DateTimeField(default=timezone.now)
    registration_end_time = models.DateTimeField(default=timezone.now)
    seller_cap = models.PositiveIntegerField(default=200)

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return f"<Event #{str(self.id)} '{self.name}', created by {self.creator.username}>"


class Announcement(models.Model):
    # foreign key
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # django "id" - automatically assigned - no need for them in models
    timestamp = models.DateTimeField(default=timezone.now)
    TITLE_MAX_LENGTH = 50
    DESCRIPTION_MAX_LENGTH = 250
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    announcement = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    picture = models.ImageField(upload_to='announcements', blank=True)

    def save(self, *args, **kwargs):
        super(Announcement, self).save(*args, **kwargs)

    def __str__(self):
        return f"<Announcement #{str(self.id)}, published by: {self.posted_by.username} at {self.timestamp}>"

# hello
