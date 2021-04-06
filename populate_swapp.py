import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'swapp_project.settings')

import django
django.setup()

from django.utils import timezone
from swapp.models import Item, Event, Checkout, Announcement
from django.contrib.auth.models import User, Group


def populate():
    checkout_time = timezone.now()
    items_jon = [
        {'name': 'Popobawa',
         'description': 'A picture of a demon that scares people',
         'price': '666.66',
         'checked': 'True',
         'picture': 'item_pictures/popobawa-demon.jpg',
         'checked_in': True,
         
         },
        {'name': 'Exclusive Water bottle 1.5l',
         'description': 'Mineral water SALVATOR - gem among waters',
         'price': '0.89',
         'checked': 'True',
         'picture': 'item_pictures/Salvator.PNG',
         'checked_in': True,
         
         },
        {'name': 'Piece of Road',
         'description': 'On sale 1.6km/1Mile piece of road',
         'price': '100000',
         'checked': 'True',
         'picture': 'item_pictures/road.jpg',
         'checked_in': True,
         
         },
    ]

    items_jane = [
        {'name': 'Louis Vuitton Designer Shoes, Women size 8.5',
         'description': 'Worn only once to impress my colleague. Didn\'t work',
         'price': '420.69',
         'picture': 'item_pictures/3.jpg',
         'checked_in': False,
         
         },
        {'name': 'Medium Neon Green Short-Sleeved T-Shirt',
         'description': 'Disputable colour. Come and see',
         'price': '12.00',
         'picture': 'item_pictures/2.jpg',
         'checked_in': False,
         
         },
    ]

    items_mark = [
        {'name': 'Grey T-Shirt Large',
         'description': '2 years old, slightly worn',
         'price': '19.99',
         'picture': 'item_pictures/1.jpg',
         'checked_in': False,
         
         },
        {'name': 'Light Grey Extra Large (XL) T-Shirt',
         'description': 'like new. Washed in Perwoll',
         'price': '39.13',
         'picture': 'item_pictures/1.jpg',
         'checked_in': False,
         
         },
        {'name': 'My Shoes size 10, Men',
         'description': 'Brand new, open box never worn',
         'price': '69.00',
         'picture': 'item_pictures/3.jpg',
         'checked_in': False,
         
         },
        {'name': 'Denim Jeans',
         'description': '2 years old, not worn at all',
         'price': '39.99',
         'picture': 'item_pictures/denim.jpg',
         'checked_in': False,
         },
        {'name': 'Jeans 44-36',
         'description': 'after my dad, too small for him',
         'price': '25.00',
         'picture': 'item_pictures/denim.jpg',
         'checked_in': False,
         
         },
        {'name': 'Some painting',
         'description': 'very rare, looked after',
         'price': '169.00',
         'picture': 'item_pictures/3bupn872myd51.jpg',
         'checked_in': False,
         
         },
    ]

    items_christie = [
        {'name': 'Small Neon Yellow Short-Sleeved T-Shirt',
         'description': 'Either Green or Yellow. Depends on your eyes. Come and see',
         'price': '10.00',
         'picture': 'item_pictures/2.jpg',
         'checked_in': True,
         
         },
        {'name': 'Red Weatherproof Jacket',
         'description': '2brand new',
         'price': '89.95',
         'picture': 'item_pictures/jacket1.jpg',
         'checked_in': True,
         
         },
        {'name': 'Blue aviator jacket',
         'description': 'Used once, too big',
         'price': '45.50',
         'picture': 'item_pictures/jacket2.jpg',
         'checked_in': False,
         },
        {'name': 'Vivid color spring jacket',
         'description': 'come and see the quality. Very nice',
         'price': '59.99',
         'picture': 'item_pictures/jacket3.jpg',
         'checked_in': True,
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

    checkouts_sam = [
        {'timestamp': timezone.now(),
         'total': '100.84',
         'paid': '120',
         'change': '19.16',
         'completed': True,
         'items': [
             {'name': 'Small Neon Yellow Short-Sleeved T-Shirt',
              'description': 'Either Green or Yellow. Depends on your eyes. Come and see',
              'price': '10.00',
              'picture': 'item_pictures/2.jpg',
              'checked_in': True,
              },
             {'name': 'Red Weatherproof Jacket',
              'description': '2brand new',
              'price': '89.95',
              'picture': 'item_pictures/jacket1.jpg',
              'checked_in': True,
              },
             {'name': 'Exclusive Water bottle 1.5l',
              'description': 'Mineral water SALVATOR - gem among waters',
              'price': '0.89',
              'checked': 'True',
              'picture': 'item_pictures/Salvator.PNG',
              'checked_in': True,
              },
         ]}
    ]

    seller_users = {
        'Jon': {'items': items_jon, 'username': 'jons12', },
        'Jane': {'items': items_jane, 'username': 'JaNeMaRy69', },
        'Mark': {'items': items_mark, 'username': 'markus', },
        'Christie': {'items': items_christie, 'username': 'yeeeter', },
    }

    staff_users = {
        'Susan': {'announcements': [],
                  'checkouts': [],
                  'events': events, },
        'Sam': {'announcements': announcements,
                'checkouts': checkouts_sam,
                'events': [], }
    }

    for seller, seller_data in seller_users.items():
        s = add_seller(seller, username=seller_data['username'])
        for i in seller_data['items']:
            add_item(s, i['name'], i['description'], i['price'], i['picture'], i['checked_in'])

    # (staff, timestamp, total, paid, change)
    for staff, staff_data in staff_users.items():
        s = add_staff(staff)
        for a in staff_data['announcements']:
            add_announcement(s, a['title'], a['description'], a['timestamp'], a['picture'])
        for c in staff_data['checkouts']:
            if not c:
                pass
            else:
                check = add_checkout(s, c['total'], c['paid'], c['change'], c['timestamp'], c['completed'])
                for i in c['items']:
                    add_item_to_checkout(i['name'], check)
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


def add_item(seller, name, description, price, picture, checked_in=False, sold_in=None):
    item = Item.objects.get_or_create(seller=seller, name=name)[0]
    item.seller = seller
    item.description = description
    item.price = price
    item.picture = picture
    item.checked = checked_in
    item.sold_in = sold_in

    item.save()
    return item


def add_item_to_checkout(name, sold_in=None):
    item = Item.objects.get_or_create(name=name)[0]
    item.sold = True
    item.sold_in = sold_in

    item.save()
    return item


def add_checkout(staff, total, paid, change, timestamp, completed):
    checkout = Checkout.objects.get_or_create(sold_by=staff, timestamp=timestamp, completed=completed)[0]
    checkout.sold_by = staff
    checkout.completed = completed
    checkout.total = total
    checkout.paid = paid
    checkout.change = change

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
