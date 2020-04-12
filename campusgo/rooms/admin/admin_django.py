from django.contrib import admin
from campusgo.rooms.models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    list_display = ['name', 'code', 'building']
