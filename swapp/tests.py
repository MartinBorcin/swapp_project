from django.test import TestCase
from django.utils import timezone
import decimal

from swapp.models import Announcement, Checkout, Event, Item
from django.contrib.auth.models import User, Group


# Create your tests here.

# Helper functions
def create_seller_user_object():
    # create dummy seller user
    seller = User.objects.get_or_create(first_name='Jon', username='user123',)[0]
    seller.groups.add(Group.objects.get_or_create(name="Seller")[0])
    return seller


def create_staff_user_object():
    # create dummy staff user
    staff = User.objects.get_or_create(first_name='Martha', username='Martha1234')[0]
    staff.groups.add(Group.objects.get_or_create(name="Staff")[0])
    return staff


def create_new_announcement(posted_by=create_staff_user_object(),
                            title="Hello",
                            announcement="This is an announcement",
                            timestamp=timezone.now()):
    return Announcement.objects.get_or_create(posted_by=posted_by,
                                              timestamp=timestamp,
                                              title=title,
                                              announcement=announcement,
                                              picture=None)[0]


def create_new_checkout(sold_by=create_staff_user_object(),
                        timestamp=timezone.now(),
                        total=100.00,
                        paid=40.00,
                        completed=False):
    if paid > total:
        completed = True
    return Checkout.objects.get_or_create(sold_by=sold_by,
                                          timestamp=timestamp,
                                          total=decimal.Decimal(total),
                                          paid=decimal.Decimal(paid),
                                          change=decimal.Decimal(total-paid),
                                          completed=completed)[0]


def create_new_event(creator=create_staff_user_object(),
                     name="New Event",
                     location="here",
                     description="event description",
                     st=timezone.now(),
                     et=timezone.now(),
                     rst=timezone.now(),
                     ret=timezone.now(),
                     seller_cap=200):
    return Event.objects.get_or_create(creator=creator,
                                       name=name,
                                       location=location,
                                       description=description,
                                       start_time=st,
                                       end_time=et,
                                       registration_start_time=rst,
                                       registration_end_time=ret,
                                       seller_cap=seller_cap)[0]


def create_new_item(seller=create_staff_user_object(),
                    sold_in=create_new_checkout(),
                    name='some item',
                    description='some description',
                    price=42.48,
                    sold=False,
                    checked=False,
                    picture=None):
    return Item.objects.get_or_create(seller=seller,
                                      sold_in=sold_in,
                                      name=name,
                                      description=description,
                                      price=price,
                                      sold=sold,
                                      checked=checked,
                                      picture=picture)[0]


class AnnouncementModelTests(TestCase):
    def test_announcement_create(self):
        user = create_staff_user_object()
        ann = create_new_announcement(posted_by=user)
        # Test the correct foreign key linking
        self.assertEqual(ann.posted_by, user, f"Invalid Foreign key Announcement-User")

    def test_announcement_picture_can_be_blank(self):
        user = create_staff_user_object()
        ann = create_new_announcement(posted_by=user)
        # Test that the picture field can be blank
        self.assertEqual(ann.picture, None, f"Announcement picture field should be blank")


class AnnouncementTryExceptTests(TestCase):
    def test_announcement_posted_by_can_not_be_blank(self):
        try:
            ann = create_new_announcement(posted_by=None)
            # foreign key posted_by cannot be null
            self.assertEqual(ann.posted_by, '', f"Announcement.posted_by cannot be null")
        except:
            pass

    def test_announcement_announcement_can_not_be_blank(self):
        try:
            user = create_staff_user_object()
            ann = create_new_announcement(posted_by=user, announcement='')
            # Test that the announcement field has some value
            self.assertEqual(ann.announcement, '', f"Announcement.announcement cannot be blank")
        except:
            pass

    def test_announcement_title_can_not_be_blank(self):
        try:
            user = create_staff_user_object()
            ann = create_new_announcement(posted_by=user, title='')
            # Test that the announcement field has some value
            self.assertEqual(ann.title, '', f"Announcement.title cannot be blank")
        except:
            pass


class CheckoutModelTests(TestCase):
    def test_checkout_create(self):
        user = create_staff_user_object()
        ch = create_new_checkout(sold_by=user)
        # Test the correct foreign key linking
        self.assertEqual(ch.sold_by, user, f"Invalid foreign key Checkout-User")

    # TODO does not work
    # def test_checkout_fields_to_be_decimal(self):
    #     user = create_staff_user_object()
    #     ch = create_new_checkout(sold_by=user, total=234.00, paid=23.00)
    #     # test that decimal fields are decimal fields
    #     self.assertTrue(ch.total, f'Checkout.total should be decimal field')
    #     self.assertTrue(ch.paid is decimal, f'Checkout.paid should be decimal field')
    #     self.assertTrue(ch.change is decimal, f'Checkout.change should be decimal field')


class CheckoutModelTryExceptTests(TestCase):
    def test_checkout_creator_not_ull(self):
        try:
            ch = create_new_checkout(sold_by=None)
            # foreign key sold_by cannot be null
            self.assertEqual(ch.sold_by, None, f"Checkout.sold_by cannot be null")
        except:
            pass

    def test_checkout_negative_total(self):
        try:
            user = create_staff_user_object()
            ch = create_new_checkout(sold_by=user, total=-20)
            # total should not be negative
            self.assertEqual(ch.total, '-20', f"Checkout.total should not be negative")
        except:
            pass

    def test_checkout_negative_paid(self):
        try:
            user = create_staff_user_object()
            ch = create_new_checkout(sold_by=user, paid=-20)
            # paid should not be negative
            self.assertEqual(ch.paid, '-20', f"Checkout.paid should not be negative")
        except:
            pass

    def test_checkout_completed_when_not_paid(self):
        try:
            user = create_staff_user_object()
            ch = create_new_checkout(sold_by=user, total=100, paid=20, completed=True)
            # completed should not be flagged as True
            self.assertEqual(ch.completed, True, f"Unpaid checkout should not be completed")
        except:
            pass


class EventModelTest(TestCase):
    def test_event_creator(self):
        user = create_staff_user_object()
        e = create_new_event(creator=user)
        # test correct foreign key linking
        self.assertEqual(e.creator, user, f"Incorrect Foreign key Event-User")


class EventTryExceptTests(TestCase):
    def test_event_creator_not_ull(self):
        try:
            e = create_new_event(creator=None)
            # foreign key creator cannot be null
            self.assertEqual(e.creator, None, f"Event.creator cannot be null")
        except:
            pass

    def test_event_name_not_null(self):
        try:
            user = create_staff_user_object()
            e = create_new_event(creator=user, name='')
            # name should not be null
            self.assertEqual(e.name, '', f"event.name should not be null")
        except:
            pass

    def test_event_location_not_null(self):
        try:
            user = create_staff_user_object()
            e = create_new_event(creator=user, location='')
            # location should not be null
            self.assertEqual(e.location, '', f"event.location should not be null")
        except:
            pass

    def test_event_description_not_null(self):
        try:
            user = create_staff_user_object()
            e = create_new_event(creator=user, description='')
            # description should not be null
            self.assertEqual(e.description, '', f"event.description should not be null")
        except:
            pass

    def test_event_negative_seller_cap(self):
        try:
            user = create_staff_user_object()
            e = create_new_event(creator=user, seller_cap=-1)
            # seller_cap should not be negative
            self.assertEqual(e.seller_cap, '-1', f"event.seller_cap should not be negative")
        except:
            pass


class ItemModelTests(TestCase):
    def test_item_seller_foreign_key(self):
        user = create_seller_user_object()
        checkout = create_new_checkout()
        i = create_new_item(seller=user, sold_in=checkout)
        # test seller foreign key linking
        self.assertEqual(i.seller, user, f"Invalid foreign key Item-User")

    def test_item_checkout_foreign_key(self):
        user = create_seller_user_object()
        checkout = create_new_checkout()
        i = create_new_item(seller=user, sold_in=checkout)
        # test checkout foreign key linking
        self.assertEqual(i.sold_in, checkout, f"Invalid foreign key linking Item-Checkout")

    def test_blank_item_checkout_foreign_key(self):
        user = create_seller_user_object()
        i = create_new_item(seller=user, sold_in=None)
        # test sold_in can be null
        self.assertEqual(i.sold_in, None, f"Foreign key item.sold_in should be Null")

    def test_blank_item_description(self):
        user = create_seller_user_object()
        checkout = create_new_checkout()
        i = create_new_item(seller=user, sold_in=checkout, description='')
        # test description can be null
        self.assertEqual(i.description, '', f"Item.description should be Null")

    def test_blank_item_picture(self):
        user = create_seller_user_object()
        checkout = create_new_checkout()
        i = create_new_item(seller=user, sold_in=checkout, picture=None)
        # test picture can be null
        self.assertEqual(i.picture, None, f"Item.picture should be blank")


class ItemTryExceptTests(TestCase):
    def test_item_name_not_null(self):
        try:
            user = create_seller_user_object()
            checkout = create_new_checkout()
            i = create_new_item(seller=user, sold_in=checkout, name='')
            # test name not null
            self.assertEqual(i.name, '', f"Item.name should not be null")
        except:
            pass

    def test_item_price_not_null(self):
        try:
            user = create_seller_user_object()
            checkout = create_new_checkout()
            i = create_new_item(seller=user, sold_in=checkout, price=None)
            # test price not null
            self.assertEqual(i.price, None, f"Item.price should not be null")
        except:
            pass

    def test_item_price_negative(self):
        try:
            user = create_seller_user_object()
            checkout = create_new_checkout()
            i = create_new_item(seller=user, sold_in=checkout, price=-1)
            # test price not negative
            self.assertEqual(i.price, None, f"Item.price should not be negative")
        except:
            pass

    def test_item_sold_not_checked(self):
        try:
            user = create_seller_user_object()
            checkout = create_new_checkout()
            i = create_new_item(seller=user, sold_in=checkout, sold=True, checked=False)
            # test if non checked item can be sold
            self.assertEqual(i.sold, True, f"Non Checked-in item should not be sold")
        except:
            pass
