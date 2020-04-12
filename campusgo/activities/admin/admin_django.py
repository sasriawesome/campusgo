from django.contrib import admin
from ..models import AcademicActivity


@admin.register(AcademicActivity)
class AcademicActivityAdmin(admin.ModelAdmin):
    search_fields = ['rmu__name', 'activity']
    list_display = ['activity', 'date_start', 'date_end', 'academic_year', 'rmu', 'status']
    raw_id_fields = ['rmu', 'academic_year']


class AcademicActivityInline(admin.TabularInline):
    extra = 0
    model = AcademicActivity
