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

def getvrflist(network):
    if network.lower() == 'emc'.lower():
        filename = '/etc/netbot/emcvrflist.txt'
    elif network.lower() == 'mtn'.lower():
        filename = '/etc/netbot/mtnvrflist.txt'

    vrfnames = []
    with open(filename) as f:
        for line in f:
            vrfnames.append(line)
    return vrfnames


@login_required
def traceroute(request):
    # task = get_object_or_404(Task, status=Task.ACTIVE)
    emcvrfname=getvrflist('emc')

    return render(request, 'traceroute/traceroute.html', {'task': "task", 'emcvrf':emcvrfname,'message':""})

@login_required
def inttraceroute(request):
    # task = get_object_or_404(Task, status=Task.ACTIVE)
    emcvrfname=getvrflist('emc')

    return render(request, 'traceroute/inttraceroute.html', {'task': "task", 'emcvrf':emcvrfname,'message':""})

@login_required()
def runtrace(request):
    sourceip = request.POST.get('sourceip')
    destip = request.POST.get('destip')
    vrf = request.POST.get('vrf')
    network = request.POST.get('network')
    vrfname = request.POST.get('vrfname')
    baseurl = get_vars('ansibengineemc')
    emcvrfname=getvrflist('emc')

    if sourceip == '' or destip == '' or vrf == '' or vrfname == '' or network == '':
        return render(request, 'traceroute/traceroute.html', {'task': "task", 'emcvrf':emcvrfname,'message':"Please fill in all the details!!"})


    if str(network).lower() == 'EMC'.lower():
        baseurl = get_vars('ansibengineemc')
    else:
        baseurl = get_vars('ansibenginemtn')

    if vrf == 'True':
        vrf="True"
    else:
        vrf="False"

    return render(request, 'traceroute/runtraceroute.html', {'sourceip': sourceip, 'destip':destip,'vrfname': vrfname, 'vrf':vrf,'baseurl':baseurl})


@login_required()
def runtraceapi(request):
    sourceip = request.POST.get('sourceip')
    destip = request.POST.get('destip')
    vrf = request.POST.get('vrf')
    vrfname = request.POST.get('vrfname')
    baseurl = request.POST.get('baseurl')

    url = baseurl+'/ansibengine/api/v1.0/runtrace'
    headers = {'content-type': 'application/json'}

    data= {}
    data['sourceip']=sourceip
    data['destip']=destip
    data['vrfname']=vrfname

    if vrf == 'True':
        data['vrf']="True"
    else:
        data['vrf']="False"
    response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
    return HttpResponse(response.text, content_type = "application/json")


@login_required()
def runinterfacetrace(request):
    routerip = request.POST.get('sourceip')
    interfaceip = request.POST.get('sourceint')
    destip = request.POST.get('destip')
    vrf = request.POST.get('vrf')
    network = request.POST.get('network')
    vrfname = request.POST.get('vrfdropdown')
    baseurl = get_vars('ansibengineemc')
    emcvrfname=getvrflist('emc')



    if routerip == '' or interfaceip == '' or destip == '' or vrf == '' or vrfname == '' or network == '':
        return render(request, 'traceroute/inttraceroute.html', {'task': "task", 'emcvrf':emcvrfname,'message':"Please fill in all the details!!"})


    if str(network).lower() == 'EMC'.lower():
        baseurl = get_vars('ansibengineemc')
    else:
        baseurl = get_vars('ansibenginemtn')

    if vrf == 'True':
        vrf="True"
    else:
        vrf="False"

    return render(request, 'traceroute/runinterfacetraceroute.html', {'routerip': routerip, 'interfaceip':interfaceip, 'destip':destip,'vrfname': vrfname, 'vrf':vrf,'baseurl':baseurl})


@login_required()
def runinterfacetraceapi(request):
    routerip = request.POST.get('routerip')
    interfaceip = request.POST.get('interfaceip')
    destip = request.POST.get('destip')
    vrf = request.POST.get('vrf')
    vrfname = request.POST.get('vrfname')
    baseurl = request.POST.get('baseurl')

    url = baseurl+'/ansibengine/api/v1.0/runinterfacetrace'
    headers = {'content-type': 'application/json'}

    data= {}
    data['routerip']=routerip
    data['interfaceip']=interfaceip
    data['destip']=destip
    data['vrfname']=vrfname

    if vrf == 'True':
        data['vrf']="True"
    else:
        data['vrf']="False"
    response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
    return HttpResponse(response.text, content_type = "application/json")


@login_required()
def gettraceroute(request):

    sourceip = request.POST.get('sourceip')
    destip = request.POST.get('destip')
    vrf = request.POST.get('vrf')
    network = request.POST.get('network')
    vrfname = request.POST.get('vrfdropdown')
    baseurl = get_vars('ansibengineemc')

    if str(network).lower() == 'EMC'.lower():
        baseurl = get_vars('ansibengineemc')
    else:
        baseurl = get_vars('ansibenginemtn')
    url = baseurl+'/ansibengine/api/v1.0/gettraceroute'
    headers = {'content-type': 'application/json'}
    emcvrfname=getvrflist('emc')

    if vrf is True:
        data= {}
        data['sourceip']=sourceip
        data['destip']=destip
        data['vrf']="True"
        data['vrfname']=vrfname

        response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
        statuscode = response.status_code
        if int(statuscode) == 200:
            return render(request, 'traceroute/traceroute.html', {'task': "task", 'emcvrf':emcvrfname, 'message':"Another task is running! Please wait.."})

    else:
        data= {}
        data['sourceip']=sourceip
        data['destip']=destip
        data['vrf']="False"
        data['vrfname']=vrfname

        response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
        statuscode = response.status_code
        if int(statuscode) == 200:
            return render(request, 'traceroute/traceroute.html', {'task': "task", 'emcvrf':emcvrfname, 'message':"Another task is running! Please wait.."})

    return render(request, 'traceroute/runtraceroute.html', {'task': "task",'baseurl':baseurl})

@login_required()
def getinterfacetraceroute(request):

    routerip = request.POST.get('sourceip')
    interfaceip = request.POST.get('sourceint')
    destip = request.POST.get('destip')
    vrf = request.POST.get('vrf')
    network = request.POST.get('network')
    vrfname = request.POST.get('vrfdropdown')
    baseurl = get_vars('ansibengineemc')

    if network.lower() == 'EMC'.lower():
        baseurl = get_vars('ansibengineemc')
    else:
        baseurl = get_vars('ansibenginemtn')
    url = baseurl+'/ansibengine/api/v1.0/getinterfacetraceroute'
    headers = {'content-type': 'application/json'}
    emcvrfname=getvrflist('emc')

    if vrf is True:
        data= {}
        data['routerip']=routerip
        data['interfaceip']=interfaceip
        data['destip']=destip
        data['vrf']="True"
        data['vrfname']=vrfname

        response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
        statuscode = response.status_code
        if int(statuscode) == 200:
            return render(request, 'traceroute/inttraceroute.html', {'task': "task", 'emcvrf':emcvrfname, 'message':"Another task is running! Please wait.."})
    else:
        data= {}
        data['routerip']=routerip
        data['interfaceip']=interfaceip
        data['destip']=destip
        data['vrf']="False"
        data['vrfname']=vrfname

        response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
        statuscode = response.status_code
        if int(statuscode) == 200:
            return render(request, 'traceroute/inttraceroute.html', {'task': "task", 'emcvrf':emcvrfname, 'message':"Another task is running! Please wait.."})
    return render(request, 'traceroute/runinterfacetraceroute.html', {'task': "task",'baseurl':baseurl})


def runtraceroute(request):
    baseurl = get_vars('ansibengineemc')
    if request.method == 'POST':
        baseurl = request.POST.get('baseurl')
    # if request.method == 'POST':
    #     baseurl = request.POST.get('baseurl')

    url = baseurl+'/ansibengine/api/v1.0/runtraceroute'
    headers = {'content-type': 'application/json'}
    data= {}
    data['value']="some"
    data['ipath']='new value'

    response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))
    return HttpResponse(response.text, content_type = "application/json")

def runinterfacetraceroute(request):
    baseurl = get_vars('ansibengineemc')
    if request.method == 'POST':
        baseurl = request.POST.get('baseurl')
    # if request.method == 'POST':
    #     baseurl = request.POST.get('baseurl')

    url = baseurl+'/ansibengine/api/v1.0/runinterfacetraceroute'
    headers = {'content-type': 'application/json'}
    data= {}
    data['value']=url

    response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))

    return HttpResponse(response.text, content_type = "application/json")
    # task = get_object_or_404(Task, status=Task.ACTIVE)
    # return render(request, 'traceroute/runtraceroute.html', {'task': "task"})

