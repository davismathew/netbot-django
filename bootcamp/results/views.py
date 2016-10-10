from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from bootcamp.results.models import Result
from bootcamp.tasks.models import Task
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from bootcamp.decorators import ajax_required
import markdown,json
from django.template.loader import render_to_string
import requests


def _results(request, results):
    paginator = Paginator(results, 10)
    baseurl="http://127.0.0.1:8000"
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    # popular_tags = Tag.get_popular_tags()
    return render(request, 'results/results.html', {
        'results': results,
        'baseurl': baseurl,
        'result': results
        # 'popular_tags': popular_tags
    })


@login_required
def results(request):
    all_results = Result.get_published()
    return _results(request, all_results)


@login_required
def result(request, slug):
    result = get_object_or_404(Result, slug=slug, status=Result.ACTIVE)
    return render(request, 'results/result.html', {'result': result})

@login_required
def cmapp(request):
    # result = get_object_or_404(Result, slug=slug, status=Result.ACTIVE)
    return render(request, 'results/cmapp.html', {'result': result})


def testpost(request):
    result=''
    if request.method == 'GET':
        result = request.POST.get('result')
        test = request.POST.get('test')
    url = 'http://200.12.221.13:5555/cmapp/api/v1.0/routerlist'
    headers = {'content-type': 'application/json'}
    data='{"title":"temp"}'
#    data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
    response = requests.post(url, data=data, headers=headers, auth=('netbot','N#tB@t'))
    data = {}
    data['something'] = response
    return HttpResponse(response.text, content_type = "application/json")
    # return render(request, 'results/result.html', {'result': response.text})


@login_required()
def resultdetails(request, id):
    # taskid=request.POST['taskid']
    # tasks = Task.objects.filter(pk=id)
    result = get_object_or_404(Result, pk=id)
    emcinventory = Result.objects.filter(network="EMC")
    mtninventory = Result.objects.filter(network="MTN")
    return render(request, 'results/result.html', {'result':result, 'emcinventory':emcinventory, 'mtninventory':mtninventory})

@login_required
def createresult(request):
    if request.method == 'POST':
        result = Result()
        result.create_user = request.user
        result.inventory = request.POST.get('inventory')
        taskid = request.POST.get('taskid')
        status = request.POST.get('status')
        if status in [Result.ACTIVE, Result.DELETED]:
            result.status = request.POST.get('status')

        if not request.POST.get('factfile'):
            result.factfile = request.POST.get('factfile')

        task = get_object_or_404(Task, pk=taskid)

        result.name = task.name
        result.description = task.description
        result.network = task.network
        result.playbook = task.playbook
        result.credential = task.credential
        # result.save()
        # tags = form.cleaned_data.get('tags')
        # task.create_tags(tags)
        # return redirect('/results/')
    return render(request, 'results/playoutput.html', {'result':159, 'taskid':taskid, 'status':status})


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
