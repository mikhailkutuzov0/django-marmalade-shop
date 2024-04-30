from django.db import models
from django.urls import reverse


class Categories(models.Model):
    """
    Модель для категорий товаров с уникальными названием и URL.

    Args:
        name (CharField): Название категории.
        slug (SlugField): URL-слаг, идентификатор для URL.
    """
    name = models.CharField(max_length=150, unique=True,
                            verbose_name='Название')
    slug = models.SlugField(max_length=250, unique=True,
                            blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Products(models.Model):
    """
    Модель продукта, содержащая информацию о товарах, включая цены, описание,
    изображение и категорию.

    Args:
        name (CharField): Название продукта.
        slug (SlugField): URL-слаг продукта.
        description (TextField): Описание продукта.
        image (ImageField): Изображение продукта.
        price (DecimalField): Цена продукта.
        discount (DecimalField): Процент скидки на продукт.
        quantity (PositiveIntegerField): Количество доступных единиц продукта.
        category (ForeignKey): Ссылка по внешнему ключу на модель категории,
                               к которой принадлежит продукт.
    """
    name = models.CharField(max_length=150, unique=True,
                            verbose_name='Название')
    slug = models.SlugField(max_length=250, unique=True,
                            blank=True, null=True, verbose_name='URL')
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images',
                              blank=True, null=True,
                              verbose_name='Изображение')
    price = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2,
        verbose_name='Скидка в процентах')
    quantity = models.PositiveIntegerField(
        default=0, verbose_name='Количество')
    category = models.ForeignKey(
        to=Categories, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id', )

    def __str__(self):
        return f'{self.name} В наличии {self.quantity}'

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'product_slug': self.slug})

    def display_id(self):
        """
        Форматирует и возвращает ID продукта в виде строки с ведущими нулями.

        Returns:
            str: ID, отформатированный с пятью символами, включая ведущие нули.
        """
        return f'{self.id:05}'

    def discounted_price(self):
        """
        Вычисляет цену товара с учетом скидки.

        Returns:
            float: Цена с учетом скидки.
        """
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price
