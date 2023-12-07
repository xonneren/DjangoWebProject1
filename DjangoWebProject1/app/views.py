"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import ObratnayaSvyaz
from django.contrib.auth.forms import UserCreationForm

from django.db import models
from .models import Blog
from .forms import BlogForm 

from .models import Comment     # использование модели комментариев
from .forms import CommentForm  # использование формы ввода комментария

from .models import Category     # использование модели категорий
from .models import Usluga     # использование модели услуг
from .forms import ZapisForm     # использование формы записи
from .models import Zayavka

from django.views.generic.detail import DetailView


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас',
            'year':datetime.now().year,
        }
    )

def obrsvyaz(request):
    assert isinstance(request, HttpRequest)
    data = None
    category = {'1': 'Запись на приём', '2': 'Информация о врачах',
                '3': 'Стоимость услуг', '4': 'Отзывы и жалобы на предоставленные услуги',
                '5': 'Другое...'}
    if request.method == 'POST':
        form = ObratnayaSvyaz(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['category'] = category[form.cleaned_data['category']]
            data['message'] = form.cleaned_data['message']
            data['number'] = form.cleaned_data['number']
            form = None
    else:
        form = ObratnayaSvyaz()
    return render(
            request,
            'app/obrsvyaz.html',
            {
                'form': form,
                'data': data
            }
    )

def registration(request):
    """Renders the registration page"""
    
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False              # запрещён вход в адм.раздел

            reg_f.is_active = True              # активный пользователь
            reg_f.is_superuser = False          # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()   # дата последней авторизации

            regform.save()                      # сохраняем изменения после добавления полей

            return redirect('home')     # переадресация на главную страницу
       
    else:
        regform = UserCreationForm()    # создание объекта формы для ввода данных
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,     # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
         }
    )

def blogpost(request, parametr):

    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit = False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        
        form = CommentForm() # создание формы для ввода комментария

        return render(
            request,
            'app/blogpost.html',
            {
                'post_1': post_1,
                'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
                'form': form, # передача формы добавления комментария в шаблон веб-страницы
                'year': datetime.now().year,
            }
    )

def newpost(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit = False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')
    else:
        
         blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',
            
            'year': datetime.now().year,
         }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',

            'year':datetime.now().year,
        }
    )

def uslugi(request, list_id = 0):
    """Renders the category page."""
    assert isinstance(request, HttpRequest)
    categories = Category.objects.all() # запрос на вывод категорий
    uslugi = Usluga.objects.filter(category_id = list_id) # применение фильтрации

    if len(uslugi) == 0:
        uslugi = Usluga.objects.all()

    return render(
        request,
        'app/uslugi.html',
        {
            'title': 'Услуги',
            'categories': categories,
            'list_selected': list_id,
            'uslugi': uslugi,
            'year': datetime.now().year,
         }
    )

def newzapis(request):
    assert isinstance(request, HttpRequest)
    data = None

    if request.method == 'POST':
        zapisform = ZapisForm(request.POST)
        if zapisform.is_valid():
            zapis_f = zapisform.save(commit=False)
            zapis_f.save()

            return redirect('newzapis')
    else:
        zapisform = ZapisForm()
    
    return render(
            request,
            'app/newzapis.html',
            {
                'zapisform': zapisform,
                'title': 'Запись на приём',
            }
    )