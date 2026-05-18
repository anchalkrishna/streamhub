from django.shortcuts import render, redirect
from .models import Streamer, Gang, StreamRequest
from .utils import get_stream_status
from django.contrib.auth.models import User


def home(request):

    # 🔥 AUTO CREATE ADMIN (ONLY ONCE)
    if not User.objects.filter(username="anchalkrishna").exists():
        User.objects.create_superuser(
            username="anchalkrishna",
            email="admin@gmail.com",
            password="anchalkerala123"
        )

    category = request.GET.get("category")
    gang_filter = request.GET.get("gang")

    streamers = Streamer.objects.all()

    # FILTER CATEGORY
    if category == "citizen":
        streamers = streamers.filter(gang__isnull=True)
    elif category == "gang":
        streamers = streamers.filter(gang__isnull=False)

    # FILTER SPECIFIC GANG
    if gang_filter:
        streamers = streamers.filter(gang_id=gang_filter)

    online = []
    offline = []

    for streamer in streamers:
        status = get_stream_status(streamer)

        if status.get("is_live"):
            online.append({
                "streamer": streamer,
                "data": status
            })
        else:
            offline.append(streamer)

    # 🔥 SORT BY VIEWERS (SAFE)
    online = sorted(
        online,
        key=lambda x: x["data"].get("viewers") or 0,
        reverse=True
    )

    gangs = Gang.objects.all()

    return render(request, "home.html", {
        "online": online,
        "offline": offline,
        "gangs": gangs,
        "category": category,
        "selected_gang": gang_filter
    })


def register(request):
    if request.method == "POST":
        StreamRequest.objects.create(
            name=request.POST.get("name"),
            platform=request.POST.get("platform"),
            channel_id=request.POST.get("channel_id"),
            category=request.POST.get("category"),
            gang_name=request.POST.get("gang_name")
        )
        return redirect("/")

    return render(request, "register.html")


def coming_soon(request):
    return render(request, "coming_soon.html")