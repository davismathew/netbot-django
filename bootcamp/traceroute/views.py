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
def traceroute(request):
    # task = get_object_or_404(Task, status=Task.ACTIVE)
    emcvrfname = []
    with open('/etc/netbot/emcvrflist.txt') as f:
        for line in f:
            emcvrfname.append(line)

    return render(request, 'traceroute/traceroute.html', {'task': "task", 'emcvrf':emcvrfname})

@login_required
def mtntraceroute(request):
    # task = get_object_or_404(Task, status=Task.ACTIVE)
    mtnvrfname = []
    with open('/etc/netbot/mtnvrflist.txt') as f:
        for line in f:
            mtnvrfname.append(line)

    return render(request, 'traceroute/mtntraceroute.html', {'task': "task", 'mtnvrf':mtnvrfname})

@login_required()
def gettraceroute(request):

    sourceip = request.POST.get('sourceip')
    destip = request.POST.get('destip')
    vrf = request.POST.get('vrf')
    network = request.POST.get('network')
    vrfname = request.POST.get('vrfdropdown')
    baseurl = 'http://200.12.221.13:5555'

    if network.lower() == 'EMC'.lower():
        baseurl = 'http://200.12.221.13:5555'
    else:
        baseurl = 'http://10.200.96.164:5555'
    url = baseurl+'/ansibengine/api/v1.0/gettraceroute'
    headers = {'content-type': 'application/json'}

    if vrf is True:
        data= {}
        data['sourceip']=sourceip
        data['destip']=destip
        data['vrf']="True"
        data['vrfname']=vrfname

        response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
    else:
        data= {}
        data['sourceip']=sourceip
        data['destip']=destip
        data['vrf']="False"
        data['vrfname']=vrfname

        response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
    return render(request, 'traceroute/runtraceroute.html', {'task': "task",'baseurl':baseurl})


def runtraceroute(request):
    baseurl = 'http://200.12.221.13:5555'
    if request.method == 'POST':
        baseurl = request.POST.get('baseurl')
    # if request.method == 'POST':
    #     baseurl = request.POST.get('baseurl')

    url = baseurl+'/ansibengine/api/v1.0/runtraceroute'
    headers = {'content-type': 'application/json'}
    data= {}
    data['value']=url

    response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))

    return HttpResponse(response.text, content_type = "application/json")
    # task = get_object_or_404(Task, status=Task.ACTIVE)
    # return render(request, 'traceroute/runtraceroute.html', {'task': "task"})

