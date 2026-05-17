from django.shortcuts import render
from .models import Streamer, Gang
from .utils import get_stream_status

def home(request):
    category = request.GET.get("category")   # citizen / gang
    gang_filter = request.GET.get("gang")    # specific gang id

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

    # 🔥 SORT BY VIEWERS (HIGHEST FIRST)
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

from .models import StreamRequest
from django.shortcuts import redirect

def register(request):
    if request.method == "POST":
        StreamRequest.objects.create(
            name=request.POST.get("name"),
            platform=request.POST.get("platform"),
            channel_id=request.POST.get("channel_id"),
            category=request.POST.get("category"),
            gang_name=request.POST.get("gang_name")
        )
        return redirect("/")   # go back to home

    return render(request, "register.html")    

def coming_soon(request):
    return render(request, "coming_soon.html")    