from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from bootcamp.tasks.models import Task
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bootcamp.tasks.forms import TaskForm
from django.contrib.auth.decorators import login_required
from bootcamp.decorators import ajax_required
import markdown
from django.template.loader import render_to_string
import requests,json


@login_required
def dispcheckipam(request):
    # task = get_object_or_404(Task, status=Task.ACTIVE)
    return render(request, 'ipam/checkipam.html', {'task': "task"})


@login_required()
def fetchipamcheck(request):

    destip = request.POST.get('destip')
    network = request.POST.get('network')
    baseurl = 'http://200.12.221.13:5555'

    if network.lower() == 'EMC'.lower():
        baseurl = 'http://200.12.221.13:5555'
    else:
        baseurl = 'http://10.200.96.164:5555'
    url = baseurl+'/ansibengine/api/v1.0/checkipam'


    return render(request, 'ipam/runcheckipam.html', {'destip': destip,'baseurl':baseurl})



def runipamcheck(request):
    baseurl = 'http://200.12.221.13:5555'
    if request.method == 'POST':
        baseurl = request.POST.get('baseurl')
        destip = request.POST.get('destip')
    # if request.method == 'POST':
    #     baseurl = request.POST.get('baseurl')

    url = baseurl+'/ansibengine/api/v1.0/checkipam'
    headers = {'content-type': 'application/json'}
    data= {}
    data['destip']= destip

    response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
    return HttpResponse(response.text, content_type = "application/json")

