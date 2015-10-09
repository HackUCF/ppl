from django.contrib import admin

from resumes.models import Resume


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('member', 'url')
    search_fields = ('member__name', 'url')


admin.site.register(Resume, ResumeAdmin)
