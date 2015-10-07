from django.contrib import admin
from membership.models import Member


class MemberAdmin(admin.ModelAdmin):
    search_fields = ('knights_email', 'preferred_email', 'name')
    list_display = ('name', 'knights_email', 'preferred_email', 'paid_dues')
    list_filter = ('paid_dues',)


admin.site.register(Member, MemberAdmin)
