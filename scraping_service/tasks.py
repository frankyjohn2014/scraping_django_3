from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab
import os

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
from asyncio import AbstractEventLoop
import datetime as dt
django.setup()
from django.db import DatabaseError
from parser import *
from scraping.models import Vacancy,City,Language,Error,Url

import requests
from bs4 import BeautifulSoup as BS
import codecs
import time
import datetime
from random import randint

headers = [{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
           'Accept':'text/html, application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8'
},
{
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'    
},
{
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
},
{
'User-Agent':'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}]
def tut_pars(start_url, city=None, language=None):
    print('run tut pars')
    session = requests.Session()
    if start_url:
        req = session.get(start_url, headers=headers[randint(0,3)])
        # print(req.status_code)
        if req.status_code == 200:
            bsObj = BS(req.content, "html.parser")
            jobs = []
            errors = []
            url = []
            base_url = 'https://jobs.tut.by'
            url.append(start_url)
            pagination = bsObj.find_all('a',attrs={'data-qa':'pager-page'})
            for link in pagination:
                link_pag = link.get('href')
                url.append(base_url + link_pag)
            time.sleep(2)
            for now_url in url:
                # print(now_url)
                all_div = bsObj.find_all('div',attrs={"class":"vacancy-serp-item"})
                if all_div:
                    for div in all_div:
                        title = div.find('a', attrs={"data-qa":"vacancy-serp__vacancy-title"}) # title #href
                        # print(title.text)
                        employer = div.find('a', attrs={"data-qa":"vacancy-serp__vacancy-employer"})
                        # print(employer.text)
                        descrp = div.find('div', attrs={"data-qa":"vacancy-serp__vacancy_snippet_responsibility"})
                        # print(descrp.text)
                        href = div.find('a', attrs={"data-qa":"vacancy-serp__vacancy-title"})
                        # print(href.get('href'))
                        logo = div.find('img', attrs={"class":"vacancy-serp-item__logo"})
                        # if logo:
                        #     print(logo.get('src'))
                        # else:
                        #     print('-')
                        # date = div.find('span', attrs={"class":"vacancy-serp-item__publication-date"}) # title #href
                        # print(date.text)
                        jobs.append({'url':href.get('href'),
                                    'title': title.text,
                                    'description':descrp.text,
                                    'company':employer.text,
                                    'city_id':city, 'language_id':language})
                else:
                    errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
            # handle = codecs.open('div.html','w', 'utf-8')
            # handle.write(str(jobs))
            # handle.close  
    return jobs,errors

def bel_pars(start_url, city=None, language=None):
    print('run bel pars')
    session = requests.Session()
    if start_url:
        req = session.get(start_url, headers=headers[randint(0,3)])
        if req.status_code == 200:
            bsObj = BS(req.content, "html.parser")
            jobs = []
            errors = []
            pag_url = []
            base_url = 'https://belmeta.com'
            # url.append(start_url)
            pagination = bsObj.find_all('a',attrs={'class':'page'})
            for link in pagination:
                link = link.get('data-href')
                links = base_url + link
                # print(links)
                if links not in pag_url:
                    pag_url.append(links)
            # print(pag_url)

            time.sleep(2)
            for now_url in pag_url:
                # print(now_url)
                req = session.get(now_url, headers=headers[randint(0,3)])
                time.sleep(2)
                bsObj = BS(req.content, "html.parser")
                all_div = bsObj.find_all('article',attrs={"class":"job"})
                # print(all_div)
                if all_div:
                    for div in all_div:
                        title_div = div.find('h2', attrs={"class":"title"})
                        title = title_div.text # title #href
                        # print(title)
                        hrefs_divs = div.find('a',href=True)
                        hrefs_div = hrefs_divs.get('href')
                        href = base_url + hrefs_div
                        # print(href)
                        company_div = div.find('div', attrs={"class":"company"})
                        company = company_div.text # title #href
                        # print(company)
                        desc_div = div.find('div', attrs={"class":"desc"})
                        decript_with_spaces = desc_div.text # title #href
                        decript = decript_with_spaces.strip()
                        # print(decript)
                        # print(decript)
                        jobs.append({'url':href,
                                    'title': title,
                                    'description':decript,
                                    'company':company,
                                    'city_id':city, 'language_id':language})
                else:
                    errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
                # handle = codecs.open('div.html','w', 'utf-8')
                # handle.write(str(jobs))
                # handle.close  
    return jobs,errors

@periodic_task(run_every=(crontab(minute='*/2')), name="run_scrap")
def start():
    print('Running')
    start = time.time()


    User = get_user_model()

    parsers = (
        (tut_pars, 'tut_pars'),
        (bel_pars, 'bel_pars')
    )
    jobs, errors = [],[]

    def get_settings():
        qs = User.objects.filter(send_email=True).values()
        print(qs)
        settings_lst = set((q['city_id'],q['language_id']) for q in qs)
        return settings_lst

    def get_urls(_settings):
        qs = Url.objects.all().values()

        url_dct = {(q['city_id'],q['language_id']): q['url_data'] for q in qs}

        urls = []
        for pair in _settings:
            if pair in url_dct:

                tmp = {}
                tmp['city'] = pair[0]
                
                tmp['language'] = pair[1]
                tmp['url_data'] = url_dct[pair]
                urls.append(tmp)
        return urls


    async def main(value):
        func, url, city, language = value
        job, err = await loop.run_in_executor(None, func, url, city, language)
        errors.extend(err)
        jobs.extend(job)

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

    loop = asyncio.get_event_loop()  #loop forever?
    tmp_tasks = [(func, data['url_data'][key],data['city'], data['language'])
                for data in url_list
                for func, key in parsers 
                ]
    if tmp_tasks:
        tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
        loop.run_until_complete(tasks)
        # loop.close()

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
        qs = Error.objects.filter(timestamp=dt.date.today())
        if qs.exists():
            err = qs.first()
            data = err.data
            err.data.update({'errors':errors})
            err.save()
        else:
            er = Error(data=f'errors:{errors}').save()


