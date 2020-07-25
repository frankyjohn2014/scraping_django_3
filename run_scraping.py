
import codecs
import os,sys
from django.contrib.auth import get_user_model
proj = os.path.dirname(os.path.abspath('manage.py')) #search way to django prj
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
from django.db.models import Q
import django
import time
import asyncio

django.setup()
from django.db import DatabaseError
from parser import *
from scraping.models import Vacancy,City,Language,Error,Url

jobs,errors = [],[]
start = time.time()
loop = asyncio.get_event_loop()





async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)

User = get_user_model()

parsers = (
    (tut_pars, 'tut_pars'),
    (bel_pars, 'bel_pars')
)

def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'],q['language_id']) for q in qs)
    return settings_lst

def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'],q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls


settings = get_settings()
url_list = get_urls(settings)






#no async function

# for data in url_list:
#     for func,key in parsers:
#         url = data['url_data'][key]

#         j,e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e
        # h = codecs.open('pars.txt', 'w', 'utf-8')
        # h.write(str(jobs))
        # h.close()
tmp_tasks = [(func, data['url_data'][key],data['city'], data['language'])
            for data in url_list
            for func, key in parsers 
            ]

tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

loop.run_until_complete(tasks)
loop.close()

#no async
# print(time.time()-start) #33sek

# print(time.time()-start) #20 sek async
for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()    
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()