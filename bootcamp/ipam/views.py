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
from bootcamp.utils.loadconfig import get_path

@login_required
def dispcheckipam(request):
    # task = get_object_or_404(Task, status=Task.ACTIVE)
    return render(request, 'ipam/checkipam.html', {'task': "task"})


@login_required()
def fetchipamcheck(request):

    destip = request.POST.get('destip')

    return render(request, 'ipam/runcheckipam.html', {'destip': destip})



def runipamcheck(request):
    emcbaseurl = get_path('ansibengineemc')
    mtnbaseurl = get_path('ansibenginemtn')
    if request.method == 'POST':
        baseurl = request.POST.get('baseurl')
        destip = request.POST.get('destip')
    # if request.method == 'POST':
    #     baseurl = request.POST.get('baseurl')

    emcurl = emcbaseurl+'/ansibengine/api/v1.0/checkipam'
    mtnurl = mtnbaseurl+'/ansibengine/api/v1.0/checkipam'
    headers = {'content-type': 'application/json'}
    data= {}
    data['destip']= destip


    emcresponse = requests.post(emcurl, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
    mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))

    temp={}
    temp['value']=json.loads(emcresponse.text)['value']+" in EMC network \n"+json.loads(mtnresponse.text)['value']+" in MTN network"

    return HttpResponse(json.dumps(temp), content_type = "application/json")

