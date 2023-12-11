from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.TextField(max_length = 100, unique_for_date = "posted", verbose_name ="Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(db_index = True, verbose_name = "Опубликовано")
    author = models.ForeignKey(User, null = True, blank = True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")

    # Методы класса
    def get_absolute_url(self): # возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])
    
    def __str__(self): # метод возвращает название, используемое для представления отдельных записей в адм. разделе
        return self.title
    
    # Метаданные - вложенный класс, который задаёт дополнительные параметры модели:

    class Meta:
        db_table = "Posts" # имя таблицы для модели
        ordering = ["-posted"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "Статья блога" # имя, под которым модель будет отображаться в адм. разделе
        verbose_name_plural = "Статьи блога"

admin.site.register(Blog)

class Comment(models.Model):
    text = models.TextField(verbose_name = "Комментарий")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата комментария")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор комментария")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья комментария")

    # Методы класса

    def __str__(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)

    #Метаданные - вложенный класс, который задаёт дополнительные параметры модели:

    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарии к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"

admin.site.register(Comment)

class Category(models.Model):
    name = models.CharField(max_length = 100, verbose_name = "Наименование категории")

    def get_absolute_url(self):
        return reverse("uslugi", args = [str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Categories" # Имя таблицы модели "Категории"
        verbose_name = "Категория услуги"
        verbose_name_plural = "Категории услуг"

admin.site.register(Category)

class Usluga(models.Model):
    name = models.CharField(max_length = 50, verbose_name = "Наименование услуги")
    description = models.TextField(verbose_name = "Описание услуги")
    price = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = "Стоимость за приём")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = "Категория")

    def get_absolute_url(self):
        return reverse("uslugi", args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Uslugi"
        verbose_name = "Услуги"
        verbose_name_plural = "Список услуг"

admin.site.register(Usluga)

class Zayavka(models.Model):
    STATUS_CHOICES = (
        ('1', 'В очереди'),
        ('2', 'Отменена'),
        ('3', 'Закрыта'),)

    user = models.ForeignKey(User, default = 1, on_delete = models.CASCADE, verbose_name = "Пользователь")
    name = models.CharField(max_length = 100, unique=True, verbose_name = "Имя клиента")
    number = models.CharField(default="+7", unique=True, max_length = 12, verbose_name = "Номер телефона для связи")
    notice = models.BooleanField(default = True, verbose_name = "Согласие на обработку персональных данных")
    status = models.CharField(max_length = 10, verbose_name = "Статус заявки", choices=STATUS_CHOICES, default = 'В очереди')

    def get_absolute_url(self):
        return reverse("newzapis", args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Zayavka"
        verbose_name = "Заявка на звонок"
        verbose_name_plural = "Заявки на звонок"
    
admin.site.register(Zayavka)

class Priem(models.Model):

    STATUS_CHOICES = (
        ('1', 'Клиент принят'),
        ('2', 'Приём отменён'),
        ('3', 'Запись подтверждена'),)

    user_name = models.ForeignKey(Zayavka, null = True, on_delete = models.CASCADE, verbose_name = "Пользователь")
    name_k = models.CharField(max_length = 100, verbose_name = "Ф.И.О. клиента")
    usluga = models.ForeignKey(Usluga, on_delete = models.CASCADE, verbose_name = "Наименование услуги")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата приёма")
    number_k = models.CharField(default="+7", unique=True, max_length = 12, verbose_name = "Номер телефона для связи")
    status = models.CharField(max_length = 10, verbose_name = "Статус заявки", choices=STATUS_CHOICES, default = '----')

    def get_absolute_url(self):
        return reverse("priems", args=[str(self.id)])

    def __str__(self):
        return str(self.name_k)

    class Meta:
        db_table = "Priems"
        verbose_name = "Запись на приём"
        verbose_name_plural = "Записи на приём"

admin.site.register(Priem)