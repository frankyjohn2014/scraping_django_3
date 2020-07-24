
import codecs
import os,sys

proj = os.path.dirname(os.path.abspath('manage.py')) #search way to django prj
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django



django.setup()
from django.db import DatabaseError
from parser import *
from scraping.models import Vacancy,City,Language,Error
parsers = (
    (tut_pars, 'https://jobs.tut.by/search/vacancy?area=1002&st=searchVacancy&fromSearch=true&text=Python'),
    (bel_pars, 'https://belmeta.com/vacansii?q=Python&l=')
)
city = City.objects.filter(slug='minsk').first()
language = Language.objects.filter(slug='python').first()
print(city)
print(language)
jobs,errors = [],[]
for func,url in parsers:
    j,e = func(url)
    jobs += j
    errors += e
    # h = codecs.open('pars.txt', 'w', 'utf-8')
    # h.write(str(jobs))
    # h.close()

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()    
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()