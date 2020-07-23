import requests
from bs4 import BeautifulSoup as BS
import codecs
import time
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
           'Accept':'text/html, application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8'
}

def tut_pars(start_url):
    session = requests.Session()
    req = session.get(start_url, headers=headers)
    bsObj = BS(req.content, "html.parser")
    jobs = []
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
        req = session.get(now_url, headers=headers)
        time.sleep(2)
        bsObj = BS(req.content, "html.parser")
        all_div = bsObj.find_all('div',attrs={"class":"vacancy-serp-item"})
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
            jobs.append({'href':href.get('href'),
                        'title': title.text,
                        'description':descrp.text,
                        'company':employer.text})

    # handle = codecs.open('div.html','w', 'utf-8')
    # handle.write(str(jobs))
    # handle.close  
    return jobs

def bel_pars(start_url):
    session = requests.Session()
    req = session.get(start_url, headers=headers)
    bsObj = BS(req.content, "html.parser")
    jobs = []
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
        req = session.get(now_url, headers=headers)
        time.sleep(2)
        bsObj = BS(req.content, "html.parser")
        all_div = bsObj.find_all('article',attrs={"class":"job"})
        # print(all_div)
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
            jobs.append({'href':href,
                        'title': title,
                        'description':decript,
                        'company':company})
    
    # handle = codecs.open('div.html','w', 'utf-8')
    # handle.write(str(jobs))
    # handle.close  
    return jobs


