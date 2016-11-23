from django.shortcuts import render
from django.template import loader, RequestContext
from django.http import HttpResponse

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'page_title': 'Cares Demo'
    })

    return HttpResponse(template.render(context))

