from datetime import datetime, timedelta, timezone
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone as tz
from django.contrib.auth.models import Group, User
from django.db.models import Sum, Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse

from swapp.forms import UserForm, AnnouncementForm, RegistrationStartTimeForm, RegistrationEndTimeForm, \
    EventStartTimeForm, EventEndTimeForm, RegistrationCapForm, EventLocationForm, EventDescriptionForm
from swapp.models import Item, Event, Announcement, Checkout
from django.contrib.auth import logout, login, authenticate

# Create your views here.


def index(request):
    # this will be replaced by database queries once models are created. For now, these are the placeholders
    announce = [
        {
            "title": "Lost and found",
            "image": 'headphones.jpeg',
            "posted_by": "staffMember1",
            "posted_at": "30 minutes ago",
            "text": "This is to remind everyone that during the entire course of event, there is a lost and found box in the staff room, so if you find anything that looks like someone might have lost it, please, do no hesitate to inform any memeber of staff. There is already a pair of headphones and a hat that have been brought. If you happened to lost them, feel free to come collect them as soon as possible.",
        },
        {
            "title": "Hello and welcome!",
            "image": None,
            "posted_by": "staffMember1",
            "posted_at": "30 minutes ago",
            "text": "Hi everyone, the event is starting in a few hours, and we are very excited to see you all again for the first time since last year! Our operation had to be temporarily suspended because of the pandemic, but now we are back on track!",
        }
    ]
    featured_items = [
        {"name": "T-shirt, grey", "image": "1.jpg", "desc": "Grey T-shirt with a picture/sign on the front; size 45", "price": "4"},
        {"name": "T-shirt, green", "image": "2.jpg", "desc": "Plain green Tshirt;size M", "price": "3"},
        {"name": "Baby shoes", "image": "3.jpg", "desc": "Baby shoes, never worn; size 16", "price": "10"}
    ]
    event_location = "Somestreet 25, 12345ZZ, Sometown, Somecountry"
    event_time = "22.01.2070 08:00 - 22.01.2070 12:00"

    announce = Announcement.objects.all()
    event = Event.objects.get(id=1)
    context_dict = {
        "announcements": announce,
        "featured_items": featured_items,
        "event": event,
    }
    return render(request, "swapp/index.html", context=context_dict)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('swapp:index'))
            else:
                return render(request, 'swapp/login.html', context={"message": "Your SwApp account is disabled."})
        else:
            print(f"Invalid login details: {username}, {password}")
            return render(request, 'swapp/login.html', context={"message": "Invalid login details supplied."})
    else:
        return render(request, 'swapp/login.html', context={"message": None})


def user_logout(request):
    logout(request)
    return redirect(reverse('swapp:index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            print(f"created user {user.username} with password {user.password}")
            seller_group = Group.objects.get(name='Seller')
            user.groups.add(seller_group)
            user.save()
            registered = True
            login(request, user)
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'swapp/register.html', context={'user_form': user_form, 'registered': registered})


def items(request):
    # TODO: display number of results
    query = request.GET.get('q', '')
    ordering = request.GET.get('order', 'name')
    if not ordering:
        ordering = 'name'
    filtered_items = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).order_by(ordering)
    paginator = Paginator(filtered_items, 2)
    page = request.GET.get('page', 1)
    items_on_page = paginator.get_page(page)
    return render(request, 'swapp/items.html', context={"search_query": query, "items": items_on_page})


def my_items(request):
    pass


def sellers(request):
    pass


def about(request):
    event = {
        "reg_start_time": "15.01.2070 08:00",
        "reg_end_time": "21.01.2070 08:00",
        "sellers_cap": 200,
        "start_time": "22.01.2070 08:00 ",
        "end_time": "22.01.2070 12:00",
    }
    return render(request, 'swapp/about.html', context={"event": event})


def get_items_sold():
    approved_items = Item.objects.filter(checked=True)
    sold_items = Item.objects.filter(sold=True)
    money_collected = sold_items.aggregate(Sum("price"))["price__sum"]
    if not money_collected:
        money_collected = 0.0
    money_earned = round(float(money_collected) * 0.25, 2)
    try:
        items_progress_percent = sold_items.count() * 100 / approved_items.count()
    except ZeroDivisionError:
        print('no approved items')
        items_progress_percent = 0
    return approved_items, sold_items, money_collected, money_earned, items_progress_percent


def refresh_status(request):
    approved_items, sold_items, money_collected, money_earned, items_progress_percent = get_items_sold()
    reg_count = User.objects.filter(groups__name__contains='Seller').count()
    reg_cap = Event.objects.get(id=1).seller_cap
    reg_progress_percent = reg_count * 100 / reg_cap
    return JsonResponse({
        "reg_count": reg_count,
        "reg_cap": reg_cap,
        "reg_progress_percent": reg_progress_percent,
        "approved_items_count": approved_items.count(),
        "sold_items_count": sold_items.count(),
        "money_collected": money_collected,
        "money_earned": money_earned,
        "items_progress_percent": items_progress_percent
    })


def manage(request):
    event = Event.objects.get(id=1)
    announcement_form = AnnouncementForm(prefix='ann-form')
    registration_start_form = RegistrationStartTimeForm(prefix='reg-start-time-form', instance=event)
    registration_end_form = RegistrationEndTimeForm(prefix='reg-end-time-form', instance=event)
    registration_cap_form = RegistrationCapForm(prefix='reg-cap-form', instance=event)
    event_start_form = EventStartTimeForm(prefix='event-start-time-form', instance=event)
    event_end_form = EventEndTimeForm(prefix='event-end-time-form', instance=event)
    event_loc_form = EventLocationForm(prefix='event-loc-form', instance=event)
    event_desc_form = EventDescriptionForm(prefix='event-desc-form', instance=event)
    if request.method == 'POST':
        print("request.POST:", request.POST)
        if "ann-form" in request.POST:
            announcement_form = AnnouncementForm(request.POST, prefix='ann-form')
            if announcement_form.is_valid():
                announcement = announcement_form.save(commit=False)
                announcement.timestamp = datetime.now(timezone.utc)
                announcement.posted_by = request.user
                if "ann-form-picture" in request.FILES:
                    announcement.picture = request.FILES["ann-form-picture"]
                announcement.save()
                return redirect(reverse("swapp:index"))
            else:
                print(announcement_form.errors)

        if 'reg-start-time-form' in request.POST:
            registration_start_form = RegistrationStartTimeForm(request.POST, prefix='reg-start-time-form', instance=event)
            if registration_start_form.is_valid():
                registration_start_form.save()
                return redirect(reverse("swapp:manage"))

        if 'reg-end-time-form' in request.POST:
            registration_end_form = RegistrationEndTimeForm(request.POST, prefix='reg-end-time-form', instance=event)
            if registration_end_form.is_valid():
                registration_end_form.save()
                return redirect(reverse("swapp:manage"))

        if 'reg-cap-form' in request.POST:
            registration_cap_form = RegistrationCapForm(request.POST, prefix='reg-cap-form', instance=event)
            if registration_cap_form.is_valid():
                registration_cap_form.save()
                return redirect(reverse("swapp:manage"))

        if 'event-start-time-form' in request.POST:
            event_start_form = EventStartTimeForm(request.POST, prefix='event-start-time-form', instance=event)
            if event_start_form.is_valid():
                event_start_form.save()
                return redirect(reverse("swapp:manage"))

        if 'event-end-time-form' in request.POST:
            event_end_form = EventEndTimeForm(request.POST, prefix='event-end-time-form', instance=event)
            if event_end_form.is_valid():
                event_end_form.save()
                return redirect(reverse("swapp:manage"))

        if 'event-loc-form' in request.POST:
            event_loc_form = EventLocationForm(request.POST, prefix='event-loc-form', instance=event)
            if event_loc_form.is_valid():
                event_loc_form.save()
                return redirect(reverse("swapp:manage"))

        if 'event-desc-form' in request.POST:
            event_desc_form = EventDescriptionForm(request.POST, prefix='event-desc-form', instance=event)
            if event_desc_form.is_valid():
                event_desc_form.save()
                return redirect(reverse("swapp:manage"))

        if 'event-start-manual' in request.POST:
            event.start_time = datetime.now(timezone.utc)
            event.save()
            return redirect(reverse("swapp:manage"))

        if 'event-end-manual' in request.POST:
            event.end_time = datetime.now(timezone.utc)
            event.save()
            return redirect(reverse("swapp:manage"))

        if 'reg-start-manual' in request.POST:
            event.registration_start_time = datetime.now(timezone.utc)
            event.save()
            return redirect(reverse("swapp:manage"))

        if 'reg-end-manual' in request.POST:
            event.registration_end_time = datetime.now(timezone.utc)
            event.save()
            return redirect(reverse("swapp:manage"))

    return render(request, "swapp/manage.html", context={
        "event_end_timestamp": event.end_time.timestamp() * 1000,
        "event_start_timestamp": event.start_time.timestamp() * 1000,
        "reg_end_timestamp": event.registration_end_time.timestamp() * 1000,
        "reg_start_timestamp": event.registration_start_time.timestamp() * 1000,
        "announcement_form": announcement_form,
        "registration_start_form": registration_start_form,
        "registration_end_form": registration_end_form,
        "registration_cap_form": registration_cap_form,
        "event_start_form": event_start_form,
        "event_end_form": event_end_form,
        "event_loc_form": event_loc_form,
        "event_desc_form": event_desc_form,
        "event": event,
    })


def select_checkout(request):
    active_sessions = Checkout.objects.filter(completed=False)
    completed_sessions = Checkout.objects.filter(completed=True)
    return render(request, "swapp/select_checkout.html", context={
        "active_sessions": active_sessions,
        "completed_sessions": completed_sessions,
        "different_user_alert": "This checkout session was started by a different user. Are you sure you want to proceed?"
    })


def new_checkout(request):
    check = Checkout.objects.create(sold_by=request.user, timestamp=tz.now())
    return redirect("swapp:checkout", checkout_id=check.id)


def checkout(request, checkout_id):
    check = Checkout.objects.get(id=checkout_id)
    checkout_items = Item.objects.filter(sold_in=check)
    total_count = checkout_items.count()

    item_id = None
    item_error = None
    paid_error = None
    if request.method == 'POST':
        if 'item-id-form' in request.POST:
            item_id = request.POST.get("item_id")
            if item_id:
                # verify if the item id is valid, e.g. if item is not already sold or in checkout or approved
                item = Item.objects.filter(id=item_id)
                if not item.exists():
                    item_error = f"Item #{item_id} does not exist."
                else:
                    item = item.get(id=item_id)
                    if not item.checked:
                        item_error = f"Item #{item_id} is not checked-in"
                    elif item.sold:
                        item_error = f"Item #{item_id} is already sold"
                    elif item.sold_in:
                        item_error = f"Item #{item_id} was already checked out in checkout #{item.sold_in.id}"
                    else:
                        item.sold_in = check
                        item.save()
                        check.total += item.price
                        check.change = round(check.paid - check.total, 2)
                        check.save()
                        return redirect('swapp:checkout', checkout_id=checkout_id)

        if 'paid-form' in request.POST:
            paid = request.POST.get("paid")
            if not paid:
                paid_error = "Please, provide an amount."
            else:
                try:
                    check.paid = Decimal(paid)
                    check.change = round(check.paid - check.total, 2)
                    check.save()
                    return redirect('swapp:checkout', checkout_id)
                except ValueError:
                    paid_error = "Please, provide a valid amount."

        if 'checkout-done' in request.POST:
            action = request.POST.get('checkout-done')

            if action == 'Confirm Payment':
                for item in checkout_items:
                    item.sold = True
                    item.save()
                check.completed = True
                check.save()
                return redirect('swapp:checkout', checkout_id)

            elif action == 'Cancel':
                for item in checkout_items:
                    item.sold_in = None
                    item.save()
                check.delete()
                return redirect('swapp:select-checkout')

        if 'remove-item' in request.POST:
            item_id = request.POST.get('item-id')
            item = checkout_items.get(id=item_id)
            item.sold_in = None
            item.save()
            check.total -= item.price
            check.change = round(check.paid - check.total, 2)
            check.save()
            return redirect('swapp:checkout', checkout_id)

    return render(request, "swapp/checkout.html", context={
        "checkout": check,
        "checkout_items": checkout_items,
        "item_id": item_id,
        "item_error": item_error,
        "total_count": total_count,
        "paid_error": paid_error,
        "cancel_warning": 'You are about to cancel this checkout, all the data will be lost. Are you sure?',
    })


def checkout_export(request, checkout_id):
    check = Checkout.objects.get(id=checkout_id)
    checkout_items = Item.objects.filter(sold_in=check)
    return render(request, "swapp/checkout_export.html", context={
        "checkout": check,
        "checkout_items": checkout_items,
        "total_count": checkout_items.count(),
    })
