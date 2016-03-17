from django.shortcuts import render, render_to_response
from django.template import RequestContext

# Create your views here.
def treemap(request, day):
    return render_to_response('multi_treemap.html', RequestContext(request))