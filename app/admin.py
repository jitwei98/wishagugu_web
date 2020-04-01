from django.contrib import admin

from .models import Event, Gift, Recipient, SuggestedGift, Permalink

# Register your models here.
admin.site.register(Event)
admin.site.register(Gift)
admin.site.register(Recipient)
admin.site.register(SuggestedGift)
admin.site.register(Permalink)
