# Create your models here.
"""
一共有书籍，作者，出版社，类别四张表

"""
from django.db import models



class Author(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Publisher(models.Model):
    name=models.CharField(max_length=40)
    city=models.CharField(max_length=40)
    def __str__(self):
        return self.name

class Book(models.Model):
    title=models.CharField(max_length=30)
    price=models.DecimalField(max_digits=6,decimal_places=3)
    pub_date=models.DateField(default='2017-01-01')
    publish=models.ForeignKey(Publisher,on_delete=models.CASCADE)
    catego=models.ManyToManyField('Category')
    auth=models.ManyToManyField(to='Author')
    def __str__(self):
        return self.title

class Category(models.Model):
    name=models.CharField(max_length=40)
    def __str__(self):
        return self.name
# class BooktoAuthor(models.Model):
#     book=models.ForeignKey(Book,on_delete=models.CASCADE)
#     auth=models.ForeignKey(Author,on_delete=models.CASCADE)




