from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from bootcamp.tasks.models import Task
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bootcamp.tasks.forms import TaskForm
from django.contrib.auth.decorators import login_required
from bootcamp.decorators import ajax_required
import markdown
from django.template.loader import render_to_string



@login_required
def traceroute(request):
    # task = get_object_or_404(Task, status=Task.ACTIVE)
    return render(request, 'traceroute/traceroute.html', {'task': "task"})

@login_required
def runtraceroute(request):
    # task = get_object_or_404(Task, status=Task.ACTIVE)
    return render(request, 'traceroute/runtraceroute.html', {'task': "task"})

