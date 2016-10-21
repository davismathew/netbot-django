from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from bootcamp.tasks.models import Task
from bootcamp.inventories.models import Inventory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bootcamp.tasks.forms import TaskForm
from django.contrib.auth.decorators import login_required
from bootcamp.decorators import ajax_required
import markdown
from django.template.loader import render_to_string
from bootcamp.utils.loadconfig import get_path

def _tasks(request, tasks):
    paginator = Paginator(tasks, 10)
    # baseurl="http://127.0.0.1:8000"
    baseurl = get_path('baseurl')
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    # popular_tags = Tag.get_popular_tags()
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks,
        'baseurl': baseurl,
        'inventory': tasks
        # 'popular_tags': popular_tags
    })


@login_required
def tasks(request):
    all_tasks = Task.get_published()
    return _tasks(request, all_tasks)


@login_required
def task(request, slug):
    task = get_object_or_404(Task, slug=slug, status=Task.ACTIVE)
    return render(request, 'tasks/task.html', {'task': task})


@login_required
def createtask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task()
            task.create_user = request.user
            task.name = form.cleaned_data.get('name')
            task.network = form.cleaned_data.get('network')
            task.playbook = form.cleaned_data.get('playbook')
            task.description = form.cleaned_data.get('description')
            task.factstatus = form.cleaned_data.get('factfilerequired')
            status = form.cleaned_data.get('status')
            if status in [Task.ACTIVE, Task.DELETED]:
                task.status = form.cleaned_data.get('status')
            task.save()
            # tags = form.cleaned_data.get('tags')
            # task.create_tags(tags)
            return redirect('/tasks/')
    else:
        form = TaskForm()
    return render(request, 'tasks/createtask.html', {'form': form})

@login_required
def edit(request, id):
    tags = ''
    if id:
        task = get_object_or_404(Task, pk=id)
        # for tag in task.get_tags():
        #     tags = u'{0} {1}'.format(tags, tag.tag)
        # tags = tags.strip()
    else:
        task = Task(create_user=request.user)

    if task.create_user.id != request.user.id:
        return redirect('home')

    if request.POST:
        form = TaskForm(request.POST, instance=task,initial={'inventory':task.pk})
        # form.fields['inventory'].queryset =
        if form.is_valid():
            form.save()
            return redirect('/tasks/')
    else:
        form = TaskForm(instance=task, initial={'tags': tags})
    return render(request, 'tasks/edit.html', {'form': form})

@login_required()
def runtask(request, id):
    # taskid=request.POST['taskid']
    # tasks = Task.objects.filter(pk=id)
    task = get_object_or_404(Task, pk=id)
    emcinventory = Inventory.objects.filter(network="EMC")
    mtninventory = Inventory.objects.filter(network="MTN")
    return render(request, 'tasks/task.html', {'task':task, 'emcinventory':emcinventory, 'mtninventory':mtninventory})

@login_required()
def listplays(request):
    temp=['new','another']
    Output={'value':temp}
    # Output

    return HttpResponse(Output, content_type = "application/json")
    # return render(request, 'results/test.html', {'result': stdoutfile})



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
