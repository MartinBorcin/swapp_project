from datetime import datetime, timezone
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone as tz
from django.contrib.auth.models import Group, User
from django.db.models import Sum, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from random import sample
from swapp.forms import UserForm, AnnouncementForm, RegistrationStartTimeForm, RegistrationEndTimeForm, \
    EventStartTimeForm, EventEndTimeForm, RegistrationCapForm, EventLocationForm, EventDescriptionForm, ItemForm
from swapp.models import Item, Event, Announcement, Checkout
from django.contrib.auth import logout, login, authenticate

# Create your views here.


def index(request):
    announce = Announcement.objects.all()
    event = Event.objects.get(id=1)
    id_selection = sample([item.id for item in Item.objects.all()], 3)
    featured_items = Item.objects.filter(id__in=id_selection)
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
                return render(request, 'swapp/login.html', context={"error": "Your SwApp account is disabled."})
        else:
            print(f"Invalid login details: {username}, {password}")
            return render(request, 'swapp/login.html', context={"error": "Invalid login details supplied."})
    else:
        return render(request, 'swapp/login.html', context={"error": None})


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


def my_items(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == "GET":
        request.q = request.GET.get('q', '')
        request.order = request.GET.get('order', 'name')
        request.page = request.GET.get('page', 1)

    if request.method == "POST":
        request.q = request.POST.get("q", "")
        request.order = request.POST.get('order', 'name')
        request.page = request.GET.get('page', 1)

        if "item_edit_form" in request.POST:
            item_id = request.POST.get('item_id')
            item = Item.objects.get(id=item_id)
            item_form = ItemForm(request.POST, prefix='item_edit_form', instance=item)
            if item_form.is_valid():
                item_form.save()

        if "item_new_form" in request.POST:
            new_item_form = ItemForm(request.POST, request.FILES, prefix="item_new_form")
            if new_item_form.is_valid():
                new_item = new_item_form.save(commit=False)
                new_item.seller = user
                # if "item_new_form_picture" in request.FILES:
                #     new_item.picture = request.FILES["item_new_form_picture"]
                new_item.save()

    user_items = Item.objects.filter(seller=user)
    filtered_items = user_items.filter(Q(name__icontains=request.q) | Q(description__icontains=request.q)).order_by(request.order)
    paginator = Paginator(filtered_items, 2)
    request.page = min((int(request.page), paginator.num_pages))
    items_on_page = paginator.get_page(request.page)

    for item in items_on_page:
        item.edit_form = ItemForm(instance=item, prefix="item_edit_form")

    new_item_form = ItemForm(prefix="item_new_form")

    return render(request, 'swapp/my-items.html', context={"items": items_on_page, "new_item_form": new_item_form, "username":username})


def check_in(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item = Item.objects.get(id=item_id)
        item.checked = not item.checked
        item.save()
        return JsonResponse({"checked_in": item.checked})


def delete_item(request):
    if request.method == "POST":
        username = request.POST.get('username')
        item_id = request.POST.get("item_id")
        item = Item.objects.get(id=item_id)
        item.delete()
        return redirect('swapp:my-items', username=username)


def sellers(request):
    query = ""
    if request.method == "GET":
        query = request.GET.get("q", "")
    all_sellers = []
    for seller in User.objects.filter(
            Q(groups__name__contains='Seller') & (Q(first_name__icontains=query) | Q(id__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query))).all():
        seller_items = Item.objects.filter(seller=seller)
        items_registered = seller_items.count()
        items_checked = seller_items.filter(checked=True).count()
        items_sold = seller_items.filter(sold=True).count()
        all_sellers.append({
            "seller": seller,
            "items_registered": items_registered,
            "items_checked": items_checked,
            'items_sold': items_sold
        })
    return render(request, 'swapp/sellers.html', context={"sellers": all_sellers})


def about(request):
    event = Event.objects.get(id=1)
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
                try:
                    # verify if the item id is valid, e.g. if item is not already sold or in checkout or approved
                    item = Item.objects.filter(id=int(item_id))
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
                except ValueError:
                    item_error = "ID must be a valid integer"

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
            print(request.POST)
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
        "confirm_cancel": 'You are about to cancel this checkout, all the data will be lost. Are you sure?',
    })


def checkout_export(request, checkout_id):
    check = Checkout.objects.get(id=checkout_id)
    checkout_items = Item.objects.filter(sold_in=check)
    return render(request, "swapp/checkout_export.html", context={
        "checkout": check,
        "checkout_items": checkout_items,
        "total_count": checkout_items.count(),
    })
