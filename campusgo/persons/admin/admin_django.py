from django.contrib import admin

from ..models import (
    Person,
    FormalEducation,
    NonFormalEducation,
    Working,
    Volunteer,
    Skill,
    Publication,
    Family,
    Award
)


class EducationLevelAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['slug', 'name', 'description']


class FormalEducationInline(admin.TabularInline):
    extra = 0
    model = FormalEducation


class NonFormalEducationInline(admin.TabularInline):
    extra = 0
    model = NonFormalEducation


class WorkingInline(admin.TabularInline):
    extra = 0
    model = Working


class OrganizationInline(admin.TabularInline):
    extra = 0
    model = Volunteer


class SkillsInline(admin.TabularInline):
    extra = 0
    model = Skill


class AwardsInline(admin.TabularInline):
    extra = 0
    model = Award


class PublicationsInline(admin.TabularInline):
    extra = 0
    model = Publication


class FamilyInline(admin.TabularInline):
    extra = 0
    model = Family


class PersonAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'date_of_birth']
    search_fields = ['fullname']
    inlines = [
        SkillsInline,
        AwardsInline,
        FormalEducationInline,
        NonFormalEducationInline,
        WorkingInline,
        OrganizationInline,
        PublicationsInline,
        FamilyInline
    ]


class FormalEducationAdmin(admin.ModelAdmin):
    list_display = ['person', 'level']


class NonFormalEducationAdmin(admin.ModelAdmin):
    list_display = ['person']


class WorkingAdmin(admin.ModelAdmin):
    list_display = ['person', 'institution']


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['person', 'organization']


class SkillsAdmin(admin.ModelAdmin):
    list_display = ['person', 'name']


class AwardsAdmin(admin.ModelAdmin):
    list_display = ['person', 'name']


class PublicationAadmin(admin.ModelAdmin):
    list_display = ['person', 'title']


class FamilyAdmin(admin.ModelAdmin):
    list_display = ['person', 'name']


admin.site.register(Person, PersonAdmin)
admin.site.register(FormalEducation, FormalEducationAdmin)
admin.site.register(NonFormalEducation, NonFormalEducationAdmin)
admin.site.register(Working, WorkingAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Skill, SkillsAdmin)
admin.site.register(Award, AwardsAdmin)
admin.site.register(Publication, PublicationAadmin)
admin.site.register(Family, FamilyAdmin)
