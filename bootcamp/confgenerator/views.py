from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bootcamp.confgenerator.forms import ConfForm,ConfTemplateForm
from bootcamp.confgenerator.models import ConfTemplate,ConfTemplateInstance
from django.contrib.auth.decorators import login_required
from bootcamp.utils.loadconfig import get_vars
import json
from play_util.AnsiblePlaybook import AnsiblePlaybook
import os.path
from bootcamp.settings import MEDIA_ROOT
from shutil import copy

def get_variables(id):
    variablesfromdb = get_object_or_404(ConfTemplate, pk=id)
    return variablesfromdb

def _listconfs(request, conftemplates):
    paginator = Paginator(conftemplates, 10)
    # baseurl="http://127.0.0.1:8000"
    page = request.GET.get('page')
    try:
        conftemplates = paginator.page(page)
    except PageNotAnInteger:
        conftemplates = paginator.page(1)
    except EmptyPage:
        conftemplates = paginator.page(paginator.num_pages)
    # popular_tags = Tag.get_popular_tags()
    return render(request, 'confgenerator/conftemplates.html', {
        'conftemplates': conftemplates,
        # 'popular_tags': popular_tags
    })


@login_required
def listconf(request):
    all_conftemps = ConfTemplate.get_published()
    return _listconfs(request, all_conftemps)



@login_required
def createconftemplate(request):
    if request.method == 'POST':
        form = ConfTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            conftemplate = ConfTemplate(jinjatemplate = request.FILES['jinjafile'],variablefile = request.FILES['variablefile'])
            conftemplate.create_user = request.user
            conftemplate.name = form.cleaned_data.get('name')
            conftemplate.playbook = form.cleaned_data.get('playbook')
            conftemplate.description = form.cleaned_data.get('description')
            status = form.cleaned_data.get('status')
            if status in [ConfTemplate.ACTIVE, ConfTemplate.DELETED]:
                conftemplate.status = form.cleaned_data.get('status')

            # variablefields = []
            # with open('/etc/variablefields.txt') as f:
    	     #    for line in f:
        	 #        variablefields.append(line.rstrip('\n'))
            # # variablefields = ["hostname","enable_pass"]
            # tempvar = json.dumps(variablefields)
            # conftemplate.variable=tempvar
            conftemplate.save()

            conftemp = get_object_or_404(ConfTemplate, pk=conftemplate.id)

            variablefields = []
            with open(str(MEDIA_ROOT)+"/"+str(conftemp.variablefile)) as f:
    	        for line in f:
        	        variablefields.append(line.rstrip('\n'))
            # variablefields = ["hostname","enable_pass"]
            tempvar = json.dumps(variablefields)
            conftemp.variable=tempvar
            conftemp.save()
            src = str(MEDIA_ROOT)+"/"+str(conftemp.jinjatemplate)
            dst = '/var/ansible/templateGen'

            try:
                copy(src,dst)
            except IOError, e:
                print "Unable to copy file. %s" % e
            # tags = form.cleaned_data.get('tags')
            # task.create_tags(tags)
            return redirect('/confgen/')
    else:
        form = ConfTemplateForm()
    return render(request, 'confgenerator/createconftemplate.html', {'form': form})

@login_required()
def downloadtemplateout(request, id):
    # taskid=request.POST['taskid']
    # tasks = Task.objects.filter(pk=id)
    confinst = get_object_or_404(ConfTemplateInstance, pk=id)
    stdoutfile = "/etc/templateout/"+confinst.confoutfilename
    fileRead = open(stdoutfile)
    Output = fileRead.read()
    Output=Output.replace("[0;32m","")
    Output=Output.replace("[0;31m","")
    Output=Output.replace("[0m"," ")
    Output=Output.replace("\x1b"," ")
    response = HttpResponse(content_type='text/plain')
    filename = 'templateout'+str(confinst.id)+str(confinst.id)
    response['Content-Disposition'] = 'attachment; filename="%s.txt"' % filename
    response.write(Output)
    return response


@login_required
def createconfinstance(request):
    if request.method == 'POST':
        # id=3
        id = request.POST.get('confid')
        variableinjson = str(get_variables(id).variable)
        variables = json.loads(variableinjson)
        form = ConfForm(request.POST or None, variables=variables)
        if form.is_valid():
            output={}
            for (key, value) in form.cleaned_data.iteritems():
                output[key]=str(value)

            del output['name']
            confinstance = ConfTemplateInstance()
            confinstance.create_user = request.user
            confinstance.name = str(get_variables(id).name)
            confinstance.varvalues = json.dumps(output)
            confinstance.conftemplate = get_object_or_404(ConfTemplate, pk=id)
            confinstance.save()
            conftemp = get_object_or_404(ConfTemplate, pk=confinstance.conftemplate.id)
            srcfilename = str(conftemp.filename()) #str(conftemp.jinjatemplate)
            destfilename = "conffile"+str(confinstance.id)+".txt"
            confinstance.confoutfilename = destfilename
            confinstance.save()
            create_playbook(output,'/var/ansible/templateGen/'+srcfilename,'/etc/templateout/'+destfilename)

            filegenstatus = 'false'
            if os.path.isfile('/etc/templateout/'+destfilename):
                filegenstatus = 'true'

            playbookName = 'EMC-Edge-RTR-Active-template.yml'
            inventory = 'dev'
            playbookinst=AnsiblePlaybook(playbookName,inventory,'/etc/ansibout/output.out')
            Output=playbookinst.runPlaybook()
            fileRead = open('/etc/ansibout/output.out')
            Output = fileRead.read()
            Output=Output.replace("[0;32m","")
            Output=Output.replace("[0;31m","")
            Output=Output.replace("[0m"," ")
            Output=Output.replace("\x1b"," ")

            # variable=form.cleaned_data.get('custom_0')
            return render(request, "confgenerator/configurations.html", {'temporary': Output, 'confid':confinstance.id, 'filegenstatus' :filegenstatus})
            # return redirect("create_user_success")
    else:
        # id=3
        id = request.GET.get('confid')
        variableinjson = str(get_variables(id).variable)
        variables = json.loads(variableinjson)
        form = ConfForm(variables=variables)

    return render(request, "confgenerator/form.html", {'form': form, 'conf': id})


def create_playbook(variables,src,dest):
    filepath = '/var/ansible' + '/templateGen/'
    target = open(filepath+'EMC-Edge-RTR-Active-template.yml', 'w')
    target.write('---')
    target.write("\n")
    target.write("- hosts: template")
    target.write("\n")
    target.write("  connection: local")
    target.write("\n")
    target.write("  vars:")
    target.write("\n")
    for key,value in variables.iteritems():
        target.write("     "+key+": "+value)
        target.write("\n")
    target.write("  tasks:")
    target.write("\n")
    target.write("  - name: GENERATE THE OUTPUT FILE")
    target.write("\n")
    target.write("    template: src="+src+" dest="+dest)


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
