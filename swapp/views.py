from django.shortcuts import render
from django.core.paginator import Paginator

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
        {"name": "T-shirt, grey", "image": "1.jpg", "desc": "Grey T-shirt with a picture/sign on the front; size 45", "price": "£4"},
        {"name": "T-shirt, green", "image": "2.jpg", "desc": "Plain green Tshirt;size M", "price": "£3"},
        {"name": "Baby shoes", "image": "3.jpg", "desc": "Baby shoes, never worn; size 16", "price": "£10"}
    ]
    event_location = "Somestreet 25, 12345ZZ, Sometown, Somecountry"
    event_time = "22.01.2070 08:00 - 22.01.2070 12:00"
    context_dict = {
        "announcements": announce,
        "featured_items": featured_items,
        "event_location": event_location,
        "event_time": event_time,
    }
    return render(request, "swapp/index.html", context=context_dict)


def login(request):
    pass


def register(request):
    pass


def items(request):
    all_items = [
        {"name": "T-shirt, grey", "image": "1.jpg", "desc": "Grey T-shirt with a picture/sign on the front; size 45", "price": 4, "available": "V (icon)"},
        {"name": "T-shirt, green", "image": "2.jpg", "desc": "Plain green Tshirt;size M", "price": 3, "available": "X (icon)"},
        {"name": "Baby shoes", "image": "3.jpg", "desc": "Baby shoes, never worn; size 16", "price": 10, "available": "? (icon)"},
        {"name": "T-shirt, grey", "image": "1.jpg", "desc": "Grey T-shirt with a picture/sign on the front; size 45", "price": 4, "available": "V (icon)"},
        {"name": "T-shirt, green", "image": "2.jpg", "desc": "Plain green Tshirt;size M", "price": 3, "available": "X (icon)"},
        {"name": "Baby shoes", "image": "3.jpg", "desc": "Baby shoes, never worn; size 16", "price": 10, "available": "? (icon)"},
        {"name": "T-shirt, grey", "image": "1.jpg", "desc": "Grey T-shirt with a picture/sign on the front; size 45", "price": 4, "available": "V (icon)"},
        {"name": "T-shirt, green", "image": "2.jpg", "desc": "Plain green Tshirt;size M", "price": 3, "available": "X (icon)"},
        {"name": "Baby shoes", "image": "3.jpg", "desc": "Baby shoes, never worn; size 16", "price": 10, "available": "? (icon)"},
    ]

    query = request.GET.get('q', '')
    filtered_items = list(filter(lambda item: query.lower() in " ".join([item['desc'], item['name']]).lower(), all_items))
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


def manage(request):
    pass
