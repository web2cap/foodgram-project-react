from django.contrib import admin
from django.db.models import Count

from .models import Recipe, RecipeIngredients, Tag


class RecipeIngredientsInstanceInline(admin.TabularInline):
    model = RecipeIngredients


class RecipeTagsInstanceInline(admin.TabularInline):
    model = Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    search_fields = ("name", "text")
    list_filter = ("author", "name", "tags")
    inlines = (RecipeIngredientsInstanceInline,)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "colour")
    search_fields = ("name", "colour")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
