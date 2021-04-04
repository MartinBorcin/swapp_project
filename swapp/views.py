from datetime import datetime, timedelta, timezone

from django.contrib.auth.models import Group, User
from django.db.models import Sum, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from swapp.forms import UserForm, AnnouncementForm, RegistrationStartTimeForm, RegistrationEndTimeForm, \
    EventStartTimeForm, EventEndTimeForm, RegistrationCapForm, EventLocationForm, EventDescriptionForm, ItemForm
from swapp.models import Item, Event, Announcement
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
    all_items = [
        {"id": 1, "name": "T-shirt, grey", "image": "1.jpg", "desc": "Grey T-shirt with a picture/sign on the front; size 45", "price": 4, "available": "V (icon)"},
        {"id": 2, "name": "T-shirt, green", "image": "2.jpg", "desc": "Plain green Tshirt;size M", "price": 3, "available": "X (icon)"},
        {"id": 3, "name": "Baby shoes", "image": "3.jpg", "desc": "Baby shoes, never worn; size 16", "price": 10, "available": "? (icon)"},
        {"id": 4, "name": "T-shirt, grey", "image": "1.jpg", "desc": "Grey T-shirt with a picture/sign on the front; size 45", "price": 4, "available": "V (icon)"},
        {"id": 5, "name": "T-shirt, green", "image": "2.jpg", "desc": "Plain green Tshirt;size M", "price": 3, "available": "X (icon)"},
        {"id": 6, "name": "Baby shoes", "image": "3.jpg", "desc": "Baby shoes, never worn; size 16", "price": 10, "available": "? (icon)"},
        {"id": 7, "name": "T-shirt, grey", "image": "1.jpg", "desc": "Grey T-shirt with a picture/sign on the front; size 45", "price": 4, "available": "V (icon)"},
        {"id": 8, "name": "T-shirt, green", "image": "2.jpg", "desc": "Plain green Tshirt;size M", "price": 3, "available": "X (icon)"},
        {"id": 9, "name": "Baby shoes", "image": "3.jpg", "desc": "Baby shoes, never worn; size 16", "price": 10, "available": "? (icon)"},
    ]

    query = request.GET.get('q', '')
    filtered_items = list(filter(lambda item: query.lower() in " ".join([item['desc'], item['name']]).lower(), all_items))
    paginator = Paginator(filtered_items, 2)
    page = request.GET.get('page', 1)
    items_on_page = paginator.get_page(page)
    return render(request, 'swapp/items.html', context={"search_query": query, "items": items_on_page})


def my_items(request,username):
    user=get_object_or_404(User, username=username)

    query = request.GET.get('q', '')
    #filtered_items = list(filter(lambda item: query.lower() in " ".join([item['desc'], item['name']]).lower(), all_items))
    
    #if django_user.groups.filter(name = Seller).exists():
    user_items = Item.objects.filter(seller=user)
        
    filtered_items = user_items.filter(Q(name__icontains = query) | Q(description__icontains = query))
    paginator = Paginator(filtered_items, 2)
    page = request.GET.get('page', 1)
    items_on_page = paginator.get_page(page)
    items = list()
    for item in items_on_page:
        item_form = ItemForm(instance = item, prefix = "item_edit_form")
        items.append({"item":item, "item_form":item_form})
        
    new_item_form = ItemForm(prefix = "item_new_form")
    
    
    if request.method == "POST":
        print(request.POST)
        if "item_edit_form" in request.POST:
            item_form = ItemForm(request.POST, prefix='item_edit_form', instance = item)
            if item_form.is_valid:
                item_form.save()
                
        if "item_new_form" in request.POST:
            new_item_form = ItemForm(request.POST, request.FILES, prefix="item_new_form")
            if new_item_form.is_valid:
                new_item = new_item_form.save(commit=False)
                new_item.seller = user
                if "item_new_form_picture" in request.FILES:
                    new_item.picture = request.FILES["item_new_form_picture"]
                new_item.save()
            
    
    return render(request, 'swapp/my-items.html', context={"search_query": query, "items": items, "new_item_form": new_item_form})

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


def manage(request):
    approved_items = Item.objects.filter(checked=True)
    sold_items = Item.objects.filter(sold=True)
    money_collected = sold_items.aggregate(Sum("price"))["price__sum"]
    if not money_collected:
        money_collected = 0.0
    money_earned = round(money_collected * 0.25, 2)
    try:
        items_progress_percent = sold_items.count()*100/approved_items.count()
    except ZeroDivisionError:
        print('no approved items')
        items_progress_percent = 0

    event = Event.objects.get(id=1)
    event_duration = max(event.end_time - event.start_time, timedelta(seconds=1))  # avoid ZeroDivisionError
    remaining_time = max(event.end_time - datetime.now(timezone.utc), timedelta(seconds=0))
    remaining_time -= timedelta(microseconds=remaining_time.microseconds)
    event_progress_percent = 100 - min(remaining_time.seconds*100/event_duration.seconds, 100)
    status = {
        "approved_items_count": approved_items.count(),
        "sold_items_count": sold_items.count(),
        "remaining_time": remaining_time,
        "time_progress": event_progress_percent,
        "money_collected": money_collected,
        "money_earned": money_earned,
        "items_progress": items_progress_percent,
    }

    # registered_sellers_count = User.objects.filter(groups__in="Seller").count()

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
                print("reg start_time: ", event.registration_start_time)
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
        "status": status,
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
