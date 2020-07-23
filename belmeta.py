import requests
from bs4 import BeautifulSoup as BS
import codecs
import time

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
           'Accept':'text/html, application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8'
}

start_url = 'https://belmeta.com/vacansii?q=python&l=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA'
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
print(pag_url)

time.sleep(2)
for now_url in pag_url:
    print(now_url)
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
        print(decript)
        jobs.append({'href':href),
                     'title': title,
                     'descript':decript,
                     'company':company})

# # # data = bsObj.prettify()#.encode('utf8')
# handle = codecs.open('div.html','w', 'utf-8')
# handle.write(str(jobs))
# handle.close  