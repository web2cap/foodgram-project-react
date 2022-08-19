from django.contrib import admin

from .models import Ingerdient


class IngerdientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("measurement_unit",)


admin.site.register(Ingerdient, IngerdientAdmin)
