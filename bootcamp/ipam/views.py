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
from bootcamp.utils.loadconfig import get_vars

@login_required
def dispcheckipam(request):
    # task = get_object_or_404(Task, status=Task.ACTIVE)
    return render(request, 'ipam/checkipam.html', {'task': "task"})


@login_required()
def fetchipamcheck(request):

    destip = request.POST.get('destip')

    return render(request, 'ipam/runcheckipam.html', {'destip': destip})



def runipamcheck(request):
    emcbaseurl = get_vars('ansibengineemc')
    mtnbaseurl = get_vars('ansibenginemtn')
    if request.method == 'POST':
        baseurl = request.POST.get('baseurl')
        destip = request.POST.get('destip')
    # if request.method == 'POST':
    #     baseurl = request.POST.get('baseurl')

    emcurl = emcbaseurl+'/ansibengine/api/v1.0/checkipam'
    mtnurl = mtnbaseurl+'/ansibengine/api/v1.0/checkipam'
    headers = {'content-type': 'application/json'}
    data= {}
    temp={}
    data['destip']= destip

    try:
        emcresponse = requests.post(emcurl, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
        mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
        if not emcresponse.status_code == 200 or not mtnresponse.status_code == 200:
            temp['value']="Error !! Unexpected response. Please report this"
            return HttpResponse(json.dumps(temp), content_type = "application/json")

    except requests.exceptions.RequestException as e:
        # return "Error: {}".format(e)
        temp['value']="Error connecting to API. Please report this"
        return HttpResponse(json.dumps(temp), content_type = "application/json")



    # if (json.loads(mtnresponse.text)['value']) is None:
    #     temp['value']="Entered Subnet :"+destip+"\n\n    On EMC Network\n\n         "+json.loads(emcresponse.text)['value']+"\n\n\n       On MTN Network\n\nApi returned null"
    #     return HttpResponse(json.dumps(temp), content_type = "application/json")
    # elif (json.loads(emcresponse.text)['value']) is None:
    #     temp['value']="Entered Subnet :"+destip+"\n\n    On MTN Network\n\n         "+json.loads(mtnresponse.text)['value']+"\n\n\n       On EMC Network\n\nApi returned null"
    #     return HttpResponse(json.dumps(temp), content_type = "application/json")


    temp['value']="Entered Subnet :"+destip+"\n\n    On EMC Network\n\n         "+json.loads(emcresponse.text)['value']+"\n\n\n       On MTN Network\n\n         "+json.loads(mtnresponse.text)['value']+" "

    return HttpResponse(json.dumps(temp), content_type = "application/json")

