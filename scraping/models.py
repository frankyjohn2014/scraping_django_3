from django.db import models
from .utils import from_cyrillic_to_eng
import jsonfield

def default_urls():
    return {"tut_pars": "", "bel_pars":""}
class City(models.Model):
    name = models.CharField(max_length=50,unique=True, verbose_name='Название населённого пункта')
    slug = models.CharField(max_length=50,unique=True, blank=True)

    class Meta:
        verbose_name = 'Название населённого пункта'
        verbose_name_plural = 'Название населённых пунктов'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args,**kwargs)    

class Language(models.Model):
    name = models.CharField(max_length=50,unique=True, verbose_name='Язык программирования')
    slug = models.CharField(max_length=50,unique=True, blank=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args,**kwargs) 

class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250,verbose_name='Заголовок вакансий')
    company = models.CharField(max_length=250,verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()

    def __str__(self):
        return str(self.timestamp)

class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ("city", "language") 