from django.contrib import admin
from .models import Streamer, Gang

admin.site.register(Streamer)
admin.site.register(Gang)

from .models import StreamRequest

admin.site.register(StreamRequest)
# Register your models here.
