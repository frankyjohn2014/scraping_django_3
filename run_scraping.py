from parser import *
import codecs


parsers = (
    (tut_pars, 'https://jobs.tut.by/search/vacancy?area=1002&st=searchVacancy&fromSearch=true&text=Python'),
    (bel_pars, 'https://belmeta.com/vacansii?q=Python&l=')
)

jobs = []
for func,url in parsers:
    j = func(url)
    jobs += j
    print(jobs)
    h = codecs.open('pars.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()

