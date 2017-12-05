from django.contrib import admin
from booksmanage import models
# Register your models here.


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass