from django.contrib import admin

from src.django_project.cast_member.models import CastMember


class CastMemberAdmin(admin.ModelAdmin):
    ...

admin.site.register(CastMember, CastMemberAdmin)
