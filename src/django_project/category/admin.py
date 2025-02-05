from django.contrib import admin

from src.django_project.category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)

