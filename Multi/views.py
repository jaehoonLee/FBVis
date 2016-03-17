from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json

fbid_sel = ""

# Create your views here.
def treemap(request, day):
    return render_to_response('multi_treemap.html', RequestContext(request))

def treemap_signal(request, day):
    global fbid_sel
    result = {"author": "Business Insider", "fbid": fbid_sel}
    return HttpResponse(json.dumps(result, indent=4, sort_keys=True))

def treemap_assign(request, fbid):
    global fbid_sel
    print fbid
    fbid_sel = fbid
    return HttpResponse()


