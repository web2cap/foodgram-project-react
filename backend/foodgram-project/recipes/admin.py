from django.contrib import admin

from .models import Resipe


class ResipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "cooking_time")
    search_fields = ("name", "text")


admin.site.register(Resipe, ResipeAdmin)
