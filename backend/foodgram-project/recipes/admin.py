from django.contrib import admin

from .models import Recipe, RecipeIngredients, Tag


class RecipeIngredientsInstanceInline(admin.TabularInline):
    model = RecipeIngredients


class RecipeTagsInstanceInline(admin.TabularInline):
    model = Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "cooking_time")
    search_fields = ("name", "text")
    inlines = (RecipeIngredientsInstanceInline,)
    tag = (RecipeTagsInstanceInline,)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "colour")
    search_fields = ("name", "colour")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
