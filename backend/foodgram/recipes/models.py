from django.db import models

from django.core.validators import (
    RegexValidator,
    MinValueValidator,
)

from users.models import User

REQUIRED_KWARGS = {'null': False, 'blank': False}


class Tag(models.Model):
    HEX_COLOR_VALIDATOR = RegexValidator(
        r'^#(?:[0-9a-fA-F]{3}){1,2}$',
        message='Неверный HEX-код цвета'
    )

    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
        **REQUIRED_KWARGS,
    )
    color = models.CharField(
        'Цветовой HEX-код',
        max_length=7,
        validators=[HEX_COLOR_VALIDATOR],
        unique=True,
        **REQUIRED_KWARGS,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True,
        **REQUIRED_KWARGS,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        **REQUIRED_KWARGS,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
    )

    def __str__(self):
        return self.name

    class Meta:
        # ordering =
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        **REQUIRED_KWARGS,
    )
    name = models.CharField(
        'Название',
        max_length=200,
        **REQUIRED_KWARGS,
    )
    text = models.TextField(
        'Описание',
        **REQUIRED_KWARGS,
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
        blank=False,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes_list',
        verbose_name='Ингредиенты',
        blank=False,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        **REQUIRED_KWARGS,
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1)],
        **REQUIRED_KWARGS,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_list',
        verbose_name='Ингридиент',
        **REQUIRED_KWARGS,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        **REQUIRED_KWARGS,
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[MinValueValidator(1)],
        **REQUIRED_KWARGS,
    )

    def __str__(self):
        return (
            f'{self.ingredient.name}: '
            f'{self.amount} ({self.ingredient.measurement_unit}) '
            f'в рецепте {self.recipe.name}'
        )

    class Meta:
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецепте'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_shopping_cart',
            )
        ]
