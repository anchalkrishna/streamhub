from django.db import models

class Gang(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Streamer(models.Model):
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('twitch', 'Twitch'),
        ('kick', 'Kick'),
    ]

    CATEGORY_CHOICES = [
        ('citizen', 'Citizen'),
        ('gang', 'Gang'),
        ('admin', 'Admin'),
    ]

    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    channel_id = models.CharField(max_length=200)

    # 🔥 NEW FIELD
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    # 🔥 FIXED (optional now)
    gang = models.ForeignKey(
        Gang,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.platform})"

class StreamRequest(models.Model):
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=20)
    channel_id = models.CharField(max_length=200)
    category = models.CharField(max_length=10)
    gang_name = models.CharField(max_length=100, null=True, blank=True)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name        
# Create your models here.
