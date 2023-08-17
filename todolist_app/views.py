from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from todolist_app.models import TaskList
from todolist_app.form import TaskForm


def index(request):
    context = {
        "welcome_text": "Welcome to Taskmate!"
    }
    return render(request, "todolist_app/index.html", context)


@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).owner = request.user
            form.save()
        messages.success(request, ("New Task Added!"))
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(
            owner=request.user).order_by('task')
        page = request.GET.get('page', 1)
        paginator = Paginator(all_tasks, 4)

        try:
            all_tasks = paginator.page(page)
        except PageNotAnInteger:
            all_tasks = paginator.page(1)
        except EmptyPage:
            all_tasks = paginator.page(paginator.num_pages)

        context = {
            "all_tasks": all_tasks,
        }
        return render(request, "todolist_app/todolist.html", context)


def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.delete()
    else:
        messages.error(request, ("Access restricted to task owner."))
    return redirect('todolist')


def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request, ("Task Updated!"))
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, "todolist_app/edit.html", {'task_obj': task_obj})


def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ("Access restricted to task owner."))
    return redirect('todolist')


def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect('todolist')


@login_required
def contact(request):
    context = {
        "welcome_text": "Contact Us"
    }
    return render(request, "todolist_app/contact.html", context)


def about(request):
    context = {
        "welcome_text": "About Us"
    }
    return render(request, "todolist_app/about.html", context)
