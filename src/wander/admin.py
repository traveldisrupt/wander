from django.contrib import admin
from wander.models import Guide, Traveler, Trip


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdmin, self).__init__(model, admin_site)


class GuideAdmin(CustomModelAdmin):
    pass


class TravelerAdmin(CustomModelAdmin):
    pass


class TripAdmin(CustomModelAdmin):
    pass


admin.site.register(Guide, GuideAdmin)
admin.site.register(Traveler, TravelerAdmin)
admin.site.register(Trip, TripAdmin)