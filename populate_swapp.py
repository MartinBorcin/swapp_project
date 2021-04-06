import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'swapp_project.settings')

import django
django.setup()

from django.utils import timezone
from swapp.models import Item, Event, Checkout, Announcement
from django.contrib.auth.models import User, Group


def populate():
    items_jon = [
        {'name': 'Popobawa',
         'description': 'A picture of a demon that scares people',
         'price': '666.66',
         'checked': 'True',
         'picture': 'item_pictures/popobawa-demon.jpg',
         },
    ]

    items_jane = [
        {'name': 'Louis Vuitton Designer Shoes, Women size 8.5',
         'description': 'Worn only once to impress my colleague. Didn\'t work',
         'price': '420.69',
         'picture': 'item_pictures/3.jpg',
         },
        {'name': 'Medium Neon Green Short-Sleeved T-Shirt',
         'description': 'Disputable colour. Come and see',
         'price': '12.00',
         'picture': 'item_pictures/2.jpg',
         },
    ]

    items_mark = [
        {'name': 'Grey T-Shirt Large',
         'description': '2 years old, slightly worn',
         'price': '19.99',
         'picture': 'item_pictures/1.jpg',
         },
        {'name': 'Light Grey Extra Large (XL) T-Shirt',
         'description': 'like new. Washed in Perwoll',
         'price': '39.13',
         'picture': 'item_pictures/1.jpg',
         },
        {'name': 'My Shoes size 10, Men',
         'description': 'Brand new, open box never worn',
         'price': '69.00',
         'picture': 'item_pictures/3.jpg',
         },
    ]

    items_christie = [
        {'name': 'Small Neon Yellow Short-Sleeved T-Shirt',
         'description': 'Either Green or Yellow. Depends on your eyes. Come and see',
         'price': '10.00',
         'picture': 'item_pictures/2.jpg',
         },
    ]

    events = [
        {'name': 'First Swapp Event',
         'location': "University of Glasgow, GMU",
         'description': "some event description here",
         'start': timezone.datetime(2021, 6, 20, 9, 0, 0, 0, timezone.utc),
         'end': timezone.datetime(2021, 6, 20, 19, 0, 0, 0, timezone.utc),
         'reg_start': timezone.datetime(2021, 5, 15, 0, 1, 0, 0, timezone.utc),
         'reg_end': timezone.datetime(2021, 6, 15, 23, 59, 0, 0, timezone.utc), },
    ]

    announcements = [
        {'title': 'Lost AirPods',
         'picture': 'announcements/headphones.jpeg',
         'description': "The person who lost these headphones in the bathroom on the second floor should come and "
                        "pick them up at the building entrance.",
         'timestamp': timezone.now(), },
    ]

    checkouts_susan = [
        {'timestamp': timezone.now(),
         'total': 123.45,
         'paid': 200.00,
         'change': 200 - 123.45, },
        {'timestamp': timezone.now(),
         'total': 10.00,
         'paid': 10.00,
         'change': 0.00, },
    ]

    checkouts_sam = [
        {'timestamp': timezone.now(),
         'total': 1.45,
         'paid': 20.00,
         'change': 20 - 1.45, },
    ]

    seller_users = {
        'Jon': {'items': items_jon, 'username': 'jons12', },
        'Jane': {'items': items_jane, 'username': 'JaNeMaRy69', },
        'Mark': {'items': items_mark, 'username': 'markus', },
        'Christie': {'items': items_christie, 'username': 'yeeeter', },
    }

    staff_users = {
        'Susan': {'announcements': [],
                  'checkouts': checkouts_susan,
                  'events': events, },
        'Sam': {'announcements': announcements,
                'checkouts': checkouts_sam,
                'events': [], }
    }

    for seller, seller_data in seller_users.items():
        s = add_seller(seller, username=seller_data['username'])
        for i in seller_data['items']:
            add_item(s, i['name'], i['description'], i['price'], i['picture'])

    # (staff, timestamp, total, paid, change)
    for staff, staff_data in staff_users.items():
        s = add_staff(staff)
        for a in staff_data['announcements']:
            add_announcement(s, a['title'], a['description'], a['timestamp'], a['picture'])
        for c in staff_data['checkouts']:
            add_checkout(s, c['timestamp'], c['total'], c['paid'], c['change'])
        for e in staff_data['events']:
            add_event(s, e['name'], e['location'], e['description'], e['start'], e['end'], e['reg_start'], e['reg_end'])


def add_seller(name, username):
    seller = User.objects.get_or_create(first_name=name)[0]
    # add the correct user role
    group = Group.objects.get_or_create(name="Seller")[0]
    seller.groups.add(group)

    seller.username = username
    seller.first_name = name

    seller.save()
    return seller


def add_staff(name):
    staff = User.objects.get_or_create(first_name=name)[0]
    staff.username = name + "123"
    staff.first_name = name
    # add the correct user role
    group = Group.objects.get_or_create(name="Staff")[0]
    staff.groups.add(group)

    staff.save()
    return staff


def add_item(seller, name, description, price, picture):
    item = Item.objects.get_or_create(seller=seller, name=name)[0]
    item.seller = seller
    item.description = description
    item.price = price
    item.picture = picture

    item.save()
    return item


def add_checkout(staff, timestamp, total, paid, change):
    checkout = Checkout.objects.get_or_create(sold_by=staff, timestamp=timestamp,
                                              total=total, paid=paid, change=change)[0]
    checkout.sold_by = staff
    # checkout.total = total
    # checkout.paid = paid
    # checkout.change = change

    checkout.save()
    return checkout


def add_event(staff, name, location, description, start, end, reg_start, reg_end):
    event = Event.objects.get_or_create(id=1)[0]
    event.creator = staff
    event.name = name
    event.location = location
    event.description = description
    event.start_time = start
    event.end_time = end
    event.registration_start_time = reg_start
    event.registration_end_time = reg_end

    event.save()
    return event


def add_announcement(staff, title, description, timestamp, picture):
    announcement = Announcement.objects.get_or_create(posted_by=staff, title=title)[0]
    announcement.posted_by = staff
    announcement.title = title
    announcement.timestamp = timestamp
    announcement.announcement = description
    announcement.picture = picture

    announcement.save()
    return announcement


# Start execution here!
if __name__ == '__main__':
    print('Starting Swapp population script...')
    populate()
