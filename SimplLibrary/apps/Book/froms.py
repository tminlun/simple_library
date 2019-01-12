# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/1/11 0011 23:25'

from django import forms
from .models import Book

class BookFrom(forms.ModelForm):
    """
    图书表单,modelform
    """
    class Meta:
        model = Book
        fields = ['name', 'publish', 'author', 'price']

