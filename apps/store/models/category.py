from django.db import models

class CategoryModel(models.Model):
    name = models.CharField(max_length=40, unique=True)
    position = models.PositiveIntegerField(default=0, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'store_categories'
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


