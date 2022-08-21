from django.contrib import admin

from .models import RecipeIngredients, Resipe


class RecipeIngredientsInstanceInline(admin.TabularInline):
    model = RecipeIngredients


class ResipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "cooking_time")
    search_fields = ("name", "text")
    inlines = (RecipeIngredientsInstanceInline,)


admin.site.register(Resipe, ResipeAdmin)
