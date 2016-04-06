from django.shortcuts import render_to_response
from django.template.context import RequestContext
from social_auth.models import *


def home(request):
    request.user.social_auth
    context = RequestContext(request, {'request':request, 'user': request.user})
    return render_to_response('social/home.html', context_instance=context)