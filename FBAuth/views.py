from django.shortcuts import render_to_response
from django.template.context import RequestContext

def home(request):
   #social = request.user.social_auth.get(provider='facebook-oauth2')
   if not request.user.is_anonymous():
      print request.user.social_auth.get(provider='facebook').extra_data['access_token']
   


   context = RequestContext(request, {'request':request, 'user': request.user})
   return render_to_response('social/home.html', context_instance=context)
