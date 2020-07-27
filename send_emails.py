import os,sys
import django
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
proj = os.path.dirname(os.path.abspath('manage.py')) #search way to django prj
sys.path.append(proj)
today = datetime.date.today()
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
django.setup()
from scraping_service.settings import EMAIL_HOST_USER

from scraping.models import Vacancy, Error, Url
ADMIN_USER = EMAIL_HOST_USER

subject = "Рассылка вакансий за {today} "
text_content = "Рассылка вакансий за {today}"
from_email = EMAIL_HOST_USER

empty = '<h2>К сожалению на сегодня Вашим предпочтениям данных нет</h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city','language','email')
users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'],i['language']),[])
    users_dct[(i['city'],i['language'])].append(i['email'])
if users_dct:
    params = {'city_id__in':[], 'language_id__in':[]}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params).values()[:10] # 10 vacancy
    qs = Vacancy.objects.filter(**params, timestamp=today).values() # vacancy today
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'],i['language_id']),[])
        vacancies[(i['city_id'],i['language_id'])].append(i)
    for keys,emails in users_dct.items():
        rows = vacancies.get(keys)
        html = ''
        for row in rows:
            html += f'<h3><a href="{ row["url"] }">{ row["title"] }</a></h3>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''

if qs.exists():
    error = qs.first()
    data = error.data

    for i in data:
        _html += f'<p><a href="{ i["url"] }">Error: { i["title"] }</a></p><br>'

    subject = "Ошибки скрапинга {today}"
    text_content = "Ошибки скрапинга"

qs = Url.objects.all().values(send_email=True).values('city','language')
urls_dct = {(i['city_id'],i['language_id']): True for i in qs}
urls_err = ''

for keys in users_dct.keys():
    if keys not in urls_dct:
        urls_err += f'<p>Для города: {keys[0]} и ЯП: {keys[1]} отсутствуют урлы</p><br>'

if urls_err:
    subject += ' Отсутствующие урлы'
    _html += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()