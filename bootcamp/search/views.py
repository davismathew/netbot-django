from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from bootcamp.feeds.models import Feed
from bootcamp.tasks.models import Task
from bootcamp.inventories.models import Inventory
from bootcamp.results.models import Result
from bootcamp.articles.models import Article
from bootcamp.questions.models import Question
from django.contrib.auth.decorators import login_required
from bootcamp.utils.loadconfig import get_vars

@login_required
def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')

        try:
            search_type = request.GET.get('type')
            if search_type not in ['results','inventories','tasks','feed', 'articles', 'questions', 'users']:
                search_type = 'tasks'

        except Exception, e:
            search_type = 'tasks'

        count = {}
        results = {}
        results['tasks'] = Task.objects.filter(name__icontains=querystring)
        results['inventories'] = Inventory.objects.filter(name__icontains=querystring)
        results['results'] = Result.objects.filter(name__icontains=querystring)
        results['feed'] = Feed.objects.filter(post__icontains=querystring,
                                              parent=None)
        results['articles'] = Article.objects.filter(
            Q(title__icontains=querystring) | Q(content__icontains=querystring)
            )
        results['questions'] = Question.objects.filter(
            Q(title__icontains=querystring) | Q(
                description__icontains=querystring))
        results['users'] = User.objects.filter(
            Q(username__icontains=querystring) | Q(
                first_name__icontains=querystring) | Q(
                    last_name__icontains=querystring))
        count['tasks'] = results['tasks'].count()
        count['inventories'] = results['inventories'].count()
        count['results'] = results['results'].count()
        count['feed'] = results['feed'].count()
        count['articles'] = results['articles'].count()
        count['questions'] = results['questions'].count()
        count['users'] = results['users'].count()
        # baseurl = "http://127.0.0.1:8000"
        baseurl = get_vars('baseurl')

        return render(request, 'search/results.html', {
            'hide_search': True,
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'baseurl': baseurl,
            'results': results[search_type],
        })
    else:
        return render(request, 'search/search.html', {'hide_search': True})
