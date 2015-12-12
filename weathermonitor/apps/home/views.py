from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext


def index(request):
    if request.method == 'GET':
        return render_to_response('weather/home.html', context_instance=RequestContext(request))
    else:
        raise Http404
