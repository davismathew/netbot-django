from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from bootcamp.inventories.models import Inventory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bootcamp.inventories.forms import InventoryForm
from django.contrib.auth.decorators import login_required
from bootcamp.decorators import ajax_required
import markdown
import requests,json
from django.template.loader import render_to_string
from bootcamp.utils.loadconfig import get_vars

@login_required
def emccm(request):
    baseurl = get_vars('baseurl')
    return render(request, 'cmapp/emccmapp.html', {'baseurl':baseurl})

@login_required
def mtncm(request):
    return render(request, 'cmapp/mtncmapp.html')

@login_required
def testmodal(request):
    return render(request, 'cmapp/task.html')


@login_required()
def coreCircuitStates(request, id):
    emcbaseurl = get_vars('ansibengineemc')
    mtnbaseurl = get_vars('ansibenginemtn')

    emcurl = 'http://200.12.221.43:5000' + '/coreCircuitStates'
    mtnurl = 'http://10.200.96.103:5000' + '/coreCircuitStates'
    headers = {'content-type': 'application/json'}
    data= {}
    temp={}
    response=''
    try:
        if id == '0':
            response = requests.post(emcurl, data=json.dumps(data), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        elif id == '1':
            response = requests.post(mtnurl, data=json.dumps(data), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        if not response.status_code == 200:
            temp['value']="Error !! Unexpected response. Please report this"
            return HttpResponse(json.dumps(temp), content_type = "application/json")


    except requests.exceptions.RequestException as e:
        # return "Error: {}".format(e)
        temp['value']="Error connecting to API. Please report this"
        return HttpResponse(json.dumps(temp), content_type = "application/json")
    return HttpResponse(response, content_type = "application/json")

@login_required()
def coreCircuitDetails(request, id):
    emcbaseurl = get_vars('ansibengineemc')
    mtnbaseurl = get_vars('ansibenginemtn')

    emcurl = 'http://200.12.221.43:5000' + '/coreCircuitDetails'
    mtnurl = 'http://10.200.96.103:5000' + '/coreCircuitDetails'
    headers = {'content-type': 'application/json'}
    data= {}
    temp={}
    response=''
    try:
        if id == '0':
            response = requests.post(emcurl, data=json.dumps(data), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        elif id == '1':
            response = requests.post(mtnurl, data=json.dumps(data), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        if not response.status_code == 200:
            temp['value']="Error !! Unexpected response. Please report this"
            return HttpResponse(json.dumps(temp), content_type = "application/json")


    except requests.exceptions.RequestException as e:
        # return "Error: {}".format(e)
        temp['value']="Error connecting to API. Please report this"
        return HttpResponse(json.dumps(temp), content_type = "application/json")
    return HttpResponse(response, content_type = "application/json")

@login_required()
def orionNodeStates(request, id):
    emcbaseurl = get_vars('ansibengineemc')
    mtnbaseurl = get_vars('ansibenginemtn')

    emcurl = 'http://200.12.221.43:5000' + '/orionNodeStates'
    mtnurl = 'http://10.200.96.103:5000' + '/orionNodeStates'
    headers = {'content-type': 'application/json'}
    data= {}
    temp={}
    response=''


    try:
        if id == '0':
            response = requests.post(emcurl, data=json.dumps(data), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        elif id == '1':
            response = requests.post(mtnurl, data=json.dumps(data), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        if not response.status_code == 200:
            temp['value']="Error !! Unexpected response. Please report this"
            return HttpResponse(json.dumps(temp), content_type = "application/json")


    except requests.exceptions.RequestException as e:
        # return "Error: {}".format(e)
        temp['value']="Error connecting to API. Please report this"
        return HttpResponse(json.dumps(temp), content_type = "application/json")
    return HttpResponse(response, content_type = "application/json")

@login_required()
def rowPingTest(request, id):
    emcbaseurl = get_vars('ansibengineemc')
    mtnbaseurl = get_vars('ansibenginemtn')
    reqbody = {}
    if request.method == 'POST':
        baseurl = request.POST.get('baseurl')
        reqbody['ca']= request.POST.get('ca')
        reqbody['cai'] = request.POST.get('cai')
        reqbody['caa'] = request.POST.get('caa')
        reqbody['cz'] = request.POST.get('cz')
        reqbody['czi'] = request.POST.get('czi')
        reqbody['cza'] = request.POST.get('cza')

    emcurl = 'http://200.12.221.43:5000' + '/rowPingTest'
    mtnurl = 'http://10.200.96.103:5000' + '/rowPingTest'
    headers = {'content-type': 'application/json'}
    data= {}
    temp={}
    response=''


    try:
        if id == '0':
            response = requests.post(emcurl, data=json.dumps(reqbody), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        elif id == '1':
            response = requests.post(mtnurl, data=json.dumps(reqbody), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        if not response.status_code == 200:
            temp['value']="Error !! Unexpected response. Please report this"
            return HttpResponse(json.dumps(temp), content_type = "application/json")

    # data["ca"] = "EMC_CORE_RAI_7606_2"
    # data["cai"] = "GigabitEthernet3/24"
    # data["caa"] = "10.10.10.71"
    # data["cz"] = "EMC_CORE_LND_7606_2"
    # data["czi"] = "GigabitEthernet1/2/1"
    # data["cza"] = "10.10.10.203"

    except requests.exceptions.RequestException as e:
        # return "Error: {}".format(e)
        temp['value']="Error connecting to API. Please report this"
        return HttpResponse(json.dumps(temp), content_type = "application/json")

    return HttpResponse(json.dumps(response), content_type = "application/json")

@login_required()
def allRowPingTest(request, id):
    emcbaseurl = get_vars('ansibengineemc')
    mtnbaseurl = get_vars('ansibenginemtn')
    reqbody = {}
    if request.method == 'POST':
        baseurl = request.POST.get('baseurl')
        reqbody['value'] = request.POST.get('value')
    # if request.method == 'POST':
    #     baseurl = request.POST.get('baseurl')
    emcurl = 'http://200.12.221.43:5000' + '/rowPingTest'
    mtnurl = 'http://10.200.96.103:5000' + '/rowPingTest'
    headers = {'content-type': 'application/json'}
    data= {}
    temp={}
    response=''
    # data["value"] = "RAI_LND_1Gig_T-SYSTEM_0EV/3_Diessen,OEV/3 Diessen 56 SCF1 . London T7 / 7LB/2 / Port 15.3,DU1400739,RAI-LND,EMC_CORE_RAI_7606_2,GigabitEthernet3/24,10.10.10.71,EMC_CORE_LND_7606_2,GigabitEthernet1/2/1,10.10.10.203,Deutsche Telekom,999-RAI-LON-102-FB-Deutsche_Telekom-(CID-0EV/3-Diessen-1),20,35,40,+49 69 20060 55 58*EMC-DIVEO-XConn-CID:5511206801-MIAMI-BRAZIL-DIVEO-10Mbps-Copper,DU0506772,DU0506772,MIAMI-BRAZIL,EMC_CORE_MIAMI_ASR_2,GigabitEthernet0/0/3.101,10.10.10.226,EMC_CORE_BRAZ_ASR1K1_1,GigabitEthernet0/0/0,10.10.10.50,T-Systems,999-MIAMI-Brazil-101-CO-TSystems-(CID:5511206801_TSYSTEMS,139,144,149,0800160066,55113097-5239"


    try:
        if id == '0':
            response = requests.post(emcurl, data=json.dumps(reqbody), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        elif id == '1':
            response = requests.post(mtnurl, data=json.dumps(reqbody), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        if not response.status_code == 200:
            temp['value']="Error !! Unexpected response. Please report this"
            return HttpResponse(json.dumps(temp), content_type = "application/json")

    except requests.exceptions.RequestException as e:
        # return "Error: {}".format(e)
        temp['value']="Error connecting to API. Please report this"
        return HttpResponse(json.dumps(temp), content_type = "application/json")

    return HttpResponse(json.dumps(response), content_type = "application/json")

@login_required()
def delCCSRecord(request, id):
    emcbaseurl = get_vars('ansibengineemc')
    mtnbaseurl = get_vars('ansibenginemtn')
    reqbody = {}

    if request.method == 'DELETE':
        baseurl = request.DELETE.get('baseurl')
        reqbody['icd']= request.DELETE.get('icd')

    emcurl = 'http://200.12.221.43:5000' + '/coreCircuitStates'
    mtnurl = 'http://10.200.96.103:5000' + '/coreCircuitStates'
    headers = {'content-type': 'application/json'}
    data= {}
    temp={}
    response=''
    data["icd"] = reqbody['icd']
    # data["icd"] = "Testing1"


    try:
        if id == '0':
            response = requests.post(emcurl, data=json.dumps(data), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        elif id == '1':
            response = requests.post(mtnurl, data=json.dumps(data), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        if not response.status_code == 200:
            temp['value']="Error !! Unexpected response. Please report this"
            return HttpResponse(json.dumps(temp), content_type = "application/json")


    except requests.exceptions.RequestException as e:
        # return "Error: {}".format(e)
        temp['value']="Error connecting to API. Please report this"
        return HttpResponse(json.dumps(temp), content_type = "application/json")
    return HttpResponse(response, content_type = "application/json")


@login_required()
def delONSRecord(request, id):
    emcbaseurl = get_vars('ansibengineemc')
    mtnbaseurl = get_vars('ansibenginemtn')
    reqbody = {}

    if request.method == 'DELETE':
        baseurl = request.DELETE.get('baseurl')
        reqbody['nodeName']= request.DELETE.get('nodeName')
        reqbody['city']= request.DELETE.get('city')

    emcurl = 'http://200.12.221.43:5000' + '/coreCircuitStates'
    mtnurl = 'http://10.200.96.103:5000' + '/coreCircuitStates'
    headers = {'content-type': 'application/json'}
    data= {}
    temp={}
    response=''
    data["icd"] = reqbody['nodeName']
    data["city"] = reqbody['city']
    # data["icd"] = "Testing1"


    try:
        if id == '0':
            response = requests.post(emcurl, data=json.dumps(data), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        elif id == '1':
            response = requests.post(mtnurl, data=json.dumps(data), headers=headers)
            # mtnresponse = requests.post(mtnurl, data=json.dumps(data), headers=headers)
        if not response.status_code == 200:
            temp['value']="Error !! Unexpected response. Please report this"
            return HttpResponse(json.dumps(temp), content_type = "application/json")


    except requests.exceptions.RequestException as e:
        # return "Error: {}".format(e)
        temp['value']="Error connecting to API. Please report this"
        return HttpResponse(json.dumps(temp), content_type = "application/json")
    return HttpResponse(response, content_type = "application/json")



# def _inventories(request, inventories):
#     paginator = Paginator(inventories, 10)
#     baseurl="http://127.0.0.1:8000"
#     page = request.GET.get('page')
#     try:
#         inventories = paginator.page(page)
#     except PageNotAnInteger:
#         inventories = paginator.page(1)
#     except EmptyPage:
#         inventories = paginator.page(paginator.num_pages)
#     # popular_tags = Tag.get_popular_tags()
#     return render(request, 'inventories/inventories.html', {
#         'inventories': inventories,
#         'baseurl': baseurl,
#         'inventory': inventories
#         # 'popular_tags': popular_tags
#     })
#
#
# @login_required
# def inventories(request):
#     all_inventories = Inventory.get_published()
#     return _inventories(request, all_inventories)
#
#
#
# @login_required
# def inventory(request, slug):
#     inventory = get_object_or_404(Inventory, slug=slug, status=Inventory.ACTIVE)
#     return render(request, 'inventories/inventory.html', {'inventory': inventory})
#
#
# @login_required
# def createinventory(request):
#     if request.method == 'POST':
#         form = InventoryForm(request.POST)
#         if form.is_valid():
#             inventory = Inventory()
#             inventory.create_user = request.user
#             inventory.name = form.cleaned_data.get('name')
#             inventory.network = form.cleaned_data.get('network')
#             inventory.playbook = form.cleaned_data.get('playbook')
#             inventory.description = form.cleaned_data.get('description')
#             inventory.factstatus = form.cleaned_data.get('factfilerequired')
#             status = form.cleaned_data.get('status')
#             if status in [Inventory.ACTIVE, Inventory.DELETED]:
#                 inventory.status = form.cleaned_data.get('status')
#             inventory.save()
#             # tags = form.cleaned_data.get('tags')
#             # task.create_tags(tags)
#             return redirect('/inventories/')
#     else:
#         form = InventoryForm()
#     return render(request, 'inventories/createinventory.html', {'form': form})
#
# @login_required
# def edit(request, id):
#     tags = ''
#     if id:
#         inventory = get_object_or_404(Inventory, pk=id)
#         # for tag in task.get_tags():
#         #     tags = u'{0} {1}'.format(tags, tag.tag)
#         # tags = tags.strip()
#     else:
#         inventory = Inventory(create_user=request.user)
#
#     if inventory.create_user.id != request.user.id:
#         return redirect('home')
#
#     if request.POST:
#         form = InventoryForm(request.POST, instance=inventory,initial={'inventory':inventory.pk})
#         # form.fields['inventory'].queryset =
#         if form.is_valid():
#             form.save()
#             return redirect('/inventories/')
#     else:
#         form = InventoryForm(instance=inventory, initial={'tags': tags})
#     return render(request, 'inventories/edit.html', {'form': form})
#
# @login_required()
# def inventorydetails(request, id):
#     # taskid=request.POST['taskid']
#     # tasks = Task.objects.filter(pk=id)
#     inventory = get_object_or_404(Inventory, pk=id)
#     emcinventory = Inventory.objects.filter(network="EMC")
#     mtninventory = Inventory.objects.filter(network="MTN")
#     return render(request, 'inventories/inventory.html', {'inventory':inventory, 'emcinventory':emcinventory, 'mtninventory':mtninventory})
#

# @login_required
# def tag(request, tag_name):
#     tags = Tag.objects.filter(tag=tag_name)
#     articles = []
#     for tag in tags:
#         if tag.article.status == Article.PUBLISHED:
#             articles.append(tag.article)
#     return _articles(request, articles)
#
#
# @login_required
# def write(request):
#     if request.method == 'POST':
#         form = ArticleForm(request.POST)
#         if form.is_valid():
#             article = Article()
#             article.create_user = request.user
#             article.title = form.cleaned_data.get('title')
#             article.content = form.cleaned_data.get('content')
#             status = form.cleaned_data.get('status')
#             if status in [Article.PUBLISHED, Article.DRAFT]:
#                 article.status = form.cleaned_data.get('status')
#             article.save()
#             tags = form.cleaned_data.get('tags')
#             article.create_tags(tags)
#             return redirect('/articles/')
#     else:
#         form = ArticleForm()
#     return render(request, 'articles/write.html', {'form': form})
#
#
# @login_required
# def drafts(request):
#     drafts = Article.objects.filter(create_user=request.user,
#                                     status=Article.DRAFT)
#     return render(request, 'articles/drafts.html', {'drafts': drafts})
#
#
# @login_required
# def edit(request, id):
#     tags = ''
#     if id:
#         article = get_object_or_404(Article, pk=id)
#         for tag in article.get_tags():
#             tags = u'{0} {1}'.format(tags, tag.tag)
#         tags = tags.strip()
#     else:
#         article = Article(create_user=request.user)
#
#     if article.create_user.id != request.user.id:
#         return redirect('home')
#
#     if request.POST:
#         form = ArticleForm(request.POST, instance=article)
#         if form.is_valid():
#             form.save()
#             return redirect('/articles/')
#     else:
#         form = ArticleForm(instance=article, initial={'tags': tags})
#     return render(request, 'articles/edit.html', {'form': form})
#
#
# @login_required
# @ajax_required
# def preview(request):
#     try:
#         if request.method == 'POST':
#             content = request.POST.get('content')
#             html = 'Nothing to display :('
#             if len(content.strip()) > 0:
#                 html = markdown.markdown(content, safe_mode='escape')
#             return HttpResponse(html)
#         else:
#             return HttpResponseBadRequest()
#
#     except Exception, e:
#         return HttpResponseBadRequest()
#
#
# @login_required
# @ajax_required
# def comment(request):
#     try:
#         if request.method == 'POST':
#             article_id = request.POST.get('article')
#             article = Article.objects.get(pk=article_id)
#             comment = request.POST.get('comment')
#             comment = comment.strip()
#             if len(comment) > 0:
#                 article_comment = ArticleComment(user=request.user,
#                                                  article=article,
#                                                  comment=comment)
#                 article_comment.save()
#             html = u''
#             for comment in article.get_comments():
#                 html = u'{0}{1}'.format(html, render_to_string('articles/partial_article_comment.html',
#                                         {'comment': comment}))
#
#             return HttpResponse(html)
#
#         else:
#             return HttpResponseBadRequest()
#
#     except Exception, e:
#         return HttpResponseBadRequest()
