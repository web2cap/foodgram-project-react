from django.contrib import admin

from .models import Recipe, RecipeIngredients, Tag


class RecipeIngredientsInstanceInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 3
    # max_num = 1
    min_num = 1


class RecipeTagsInstanceInline(admin.TabularInline):
    model = Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "favorite_count")
    search_fields = (
        "name",
        "text",
        "author__username",
        "author__first_name",
        "author__last_name",
        "tags__name",
        "tags__slug",
    )
    list_filter = ("author", "tags")
    inlines = (RecipeIngredientsInstanceInline,)

    def favorite_count(self, obj):
        return obj.favorite_count


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")
    search_fields = ("name", "color")


class RecipeIngredientsAdmin(admin.ModelAdmin):
    search_fields = ("ingredient__name", "recipe__name")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
