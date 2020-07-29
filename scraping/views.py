from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

def home_view(request):
    print(request.GET)
    form = FindForm()

    return render(request,'scraping/home.html', {'form':form})


def list_view(request):
    # print(request.GET)
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    page_obj = []
    context = {'city': city, 'language':language, 'form':form}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)

        paginator = Paginator(qs, 10) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request,'scraping/list.html', context)


class DView(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'scraping/detail_view.html'

class VList(ListView):
    model = Vacancy
    template_name = 'scraping/list.html'
    form = FindForm() 
    paginate_by = 6
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form
        return context
    
    def get_queryset(self, **kwargs):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language

            qs = Vacancy.objects.filter(**_filter)
        return qs