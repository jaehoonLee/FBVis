from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

fbid_sel = ""

pal_col1 = [];
pal_col2 = [];
pal_col3 = [];
pal_col4 = [];

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

def pallette(request):
    return render_to_response('pallette.html', RequestContext(request))

def pallette_signal(request):
    global pal_col1
    global pal_col2
    global pal_col3
    global pal_col4

    result = {'1':pal_col1, '2':pal_col2, '3':pal_col3, '4':pal_col4}

    return HttpResponse(json.dumps(result, indent=4, sort_keys=True))


@csrf_exempt
def pallette_assign(request):
    global pal_col1
    global pal_col2
    global pal_col3
    global pal_col4

    col = int(request.POST['col'])
    author = request.POST['author']

    if author in pal_col1:
        pal_col1.remove(author)
    if author in pal_col2:
        pal_col2.remove(author)
    if author in pal_col3:
        pal_col3.remove(author)
    if author in pal_col4:
        pal_col4.remove(author)

    if col == 1:
        pal_col1.append(author)
    elif col == 2:
        pal_col2.append(author)
    elif col == 3:
        pal_col3.append(author)
    elif col == 4:
        pal_col4.append(author)


    print pal_col1
    print pal_col2
    print pal_col3
    print pal_col4

    result = {}

    return HttpResponse(json.dumps(result, indent=4, sort_keys=True))





