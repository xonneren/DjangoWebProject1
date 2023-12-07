"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from django.db import models
from .models import Comment
from .models import Blog
from .models import Priem
from .models import Zayavka

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Логин'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class ObratnayaSvyaz(forms.Form):
    name = forms.CharField(label = 'Ваше имя', min_length = 2, max_length = 100)
    city = forms.CharField(label = 'Место проживания', min_length =2, max_length = 100)
    category = forms.ChoiceField(label = 'Выберите категорию обращения',
                                 choices = (('1', 'Запись на приём'),
                                            ('2', 'Информация о врачах'),
                                            ('3', 'Стоимость услуг'),
                                            ('4', 'Отзывы и жалобы на предоставленные услуги'),
                                            ('5', 'Другое...')), initial = 1)
    message = forms.CharField(label = 'Ваше сообщение', widget = forms.Textarea(attrs = {'rows': 12, 'cols': 60}))
    number = forms.CharField(label = 'Введите номер телефона для связи', min_length = 12)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment         # используемая модель
        fields = ('text',)      # требуется заполнять только поля текст
        labels = {'text': "Комментарий"}    # метка к полю формы text

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка"}

class ZapisForm(forms.ModelForm):
    class Meta:
        model = Zayavka
        fields = ('name', 'number', 'notice')
        labels = {'name': "Имя клиента", 'number': "Номер телефона", 'notice': "Согласен(-на) с условиями предоставления услуг и обработки персональных данных"}


class PriemForm(forms.ModelForm):
    class Meta:
        model = Priem
        fields = ('name_k', 'usluga', 'date', 'number_k', 'status')
        labels = {'name_k': "Ф.И.О", 'usluga': "Наименование услуги", 'date': "Дата приёма", 'number_k': "Номер телефона для связи", 'status': "Статус"}