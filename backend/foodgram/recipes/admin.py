from django.contrib import admin

from .models import (
    Favourite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,

)

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(IngredientInRecipe)
admin.site.register(ShoppingCart)
admin.site.register(Favourite)
