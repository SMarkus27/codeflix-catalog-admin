from django.contrib import admin

from src.django_project.genre.models import Genre


class GenreAdmin(admin.ModelAdmin):
    pass

admin.site.register(Genre, GenreAdmin)
