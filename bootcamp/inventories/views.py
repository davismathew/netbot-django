from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from bootcamp.inventories.models import Inventory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bootcamp.inventories.forms import InventoryForm
from django.contrib.auth.decorators import login_required
from bootcamp.decorators import ajax_required
import markdown
from django.template.loader import render_to_string
import requests, json
from bootcamp.utils.loadconfig import get_path


def _inventories(request, inventories):
    paginator = Paginator(inventories, 10)
    # baseurl="http://127.0.0.1:8000"
    baseurl = get_path('baseurl')
    page = request.GET.get('page')
    try:
        inventories = paginator.page(page)
    except PageNotAnInteger:
        inventories = paginator.page(1)
    except EmptyPage:
        inventories = paginator.page(paginator.num_pages)
    # popular_tags = Tag.get_popular_tags()
    return render(request, 'inventories/inventories.html', {
        'inventories': inventories,
        'baseurl': baseurl,
        'inventory': inventories
        # 'popular_tags': popular_tags
    })


@login_required
def inventories(request):
    all_inventories = Inventory.get_published()
    return _inventories(request, all_inventories)


@login_required
def inventory(request, slug):
    inventory = get_object_or_404(Inventory, slug=slug, status=Inventory.ACTIVE)
    return render(request, 'inventories/inventory.html', {'inventory': inventory})


@login_required
def createinventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = Inventory()
            inventory.create_user = request.user
            inventory.name = form.cleaned_data.get('name')
            inventory.network = form.cleaned_data.get('network')
            inventory.playbook = form.cleaned_data.get('playbook')
            inventory.variable = form.cleaned_data.get('variable')
            inventory.description = form.cleaned_data.get('description')
            inventory.factstatus = form.cleaned_data.get('factfilerequired')
            status = form.cleaned_data.get('status')
            if status in [Inventory.ACTIVE, Inventory.DELETED]:
                inventory.status = form.cleaned_data.get('status')
            inventory.save()
            ansibengineemc = get_path('ansibengineemc')
            ansibenginemtn = get_path('ansibenginemtn')

            if inventory.network == 'EMC':
                url = ansibengineemc+'/ansibengine/api/v1.0/altinventory'
            else:
                url = ansibenginemtn+'/ansibengine/api/v1.0/altinventory'

            # url = 'http://200.12.221.13:5555/ansibengine/api/v1.0/altinventory'
            headers = {'content-type': 'application/json'}
            data= {}
            data['variable']= form.cleaned_data.get('name')
            data['inventory']= form.cleaned_data.get('variable')

            # data='{"variable":"10.10.10.102"}'
#    data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
            response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))

            # tags = form.cleaned_data.get('tags')
            # task.create_tags(tags)
            return redirect('/inventories/')
    else:
        form = InventoryForm()
    return render(request, 'inventories/createinventory.html', {'form': form})

@login_required
def edit(request, id):
    tags = ''
    if id:
        inventory = get_object_or_404(Inventory, pk=id)
        # for tag in task.get_tags():
        #     tags = u'{0} {1}'.format(tags, tag.tag)
        # tags = tags.strip()
    else:
        inventory = Inventory(create_user=request.user)

    if inventory.create_user.id != request.user.id:
        return redirect('home')

    if request.POST:
        form = InventoryForm(request.POST, instance=inventory,initial={'inventory':inventory.pk})
        # form.fields['inventory'].queryset =
        invinstance = get_object_or_404(Inventory, pk=id)
        if form.is_valid():
            form.save()
            ansibengineemc = get_path('ansibengineemc')
            ansibenginemtn = get_path('ansibenginemtn')

            if invinstance.network == 'EMC':
                url = ansibengineemc+'/ansibengine/api/v1.0/altinventory'
            else:
                url = ansibenginemtn+'/ansibengine/api/v1.0/altinventory'
            # url = 'http://200.12.221.13:5555/ansibengine/api/v1.0/altinventory'
            headers = {'content-type': 'application/json'}
            data= {}
            data['variable']= form.cleaned_data.get('name')
            data['inventory']= form.cleaned_data.get('variable')
            # data='{"variable":"10.10.10.102","inventory":invinstance}'
#    data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
            response = requests.post(url, data=json.dumps(data), headers=headers, auth=('netbot','N#tB@t'))

            return redirect('/inventories/')
    else:
        form = InventoryForm(instance=inventory, initial={'tags': tags})
    return render(request, 'inventories/edit.html', {'form': form})

@login_required()
def inventorydetails(request, id):
    # taskid=request.POST['taskid']
    # tasks = Task.objects.filter(pk=id)
    inventory = get_object_or_404(Inventory, pk=id)
    emcinventory = Inventory.objects.filter(network="EMC")
    mtninventory = Inventory.objects.filter(network="MTN")
    return render(request, 'inventories/inventory.html', {'inventory':inventory, 'emcinventory':emcinventory, 'mtninventory':mtninventory})


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
