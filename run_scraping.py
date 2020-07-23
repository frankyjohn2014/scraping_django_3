
import codecs
import os,sys

proj = os.path.dirname(os.path.abspath('manage.py')) #search way to django prj
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django


django.setup()

from parser import *
from scraping.models import Vacancy,City,Language
parsers = (
    (tut_pars, 'https://jobs.tut.by/search/vacancy?area=1002&st=searchVacancy&fromSearch=true&text=Python'),
    (bel_pars, 'https://belmeta.com/vacansii?q=Python&l=')
)
city = City.objects.filter(slug='minsk')
print(city)
jobs = []
for func,url in parsers:
    j = func(url)
    jobs += j
    # h = codecs.open('pars.txt', 'w', 'utf-8')
    # h.write(str(jobs))
    # h.close()

