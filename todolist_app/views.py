from django.shortcuts import render,redirect
from todolist_app.models import tasklist 
from todolist_app.forms import taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method =="POST":
        form=taskform(request.POST or None)
        if form.is_valid:
            instance=form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request,("Task Added"))
        return redirect('todolist')
    else:
        
        all_tasks=tasklist.objects.filter(manage=request.user)
        paginator=Paginator(all_tasks,5)
        page=request.GET.get('pg')    
        all_tasks=paginator.get_page(page)
        return render(request,'todolist.html',{'all_tasks':all_tasks})

@login_required
def delete_task(request,task_id):
    task=tasklist.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request,("Access Denied!"))      

    
    return redirect('todolist')

@login_required
def complete_task(request,task_id):
    task=tasklist.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done=True
        task.save()
    else:
        messages.error(request,("Access Denied!"))   
    return redirect('todolist')

@login_required
def pending_task(request,task_id):
    task=tasklist.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done=False
        task.save()
    else:
        messages.error(request,("Access Denied!"))  
    return redirect('todolist')


@login_required
def edit_task(request,task_id):    
    if request.method =="POST":
        task=tasklist.objects.get(pk=task_id)
        form=taskform(request.POST or None,instance=task)
        if form.is_valid:            
            form.save()
        messages.success(request,("Task Edited!"))               
        return redirect('todolist')
    else:
        
        task_object=tasklist.objects.get(pk=task_id)    
        return render(request,'edit.html',{'task_object':task_object})
    
def index(request):
    context = {
        'index_text':"Welcome index Page.",
        }
    return render(request, 'index.html', context)
@login_required
def contact(request):
    context = {
        'contact_text':"Welcome Contact Page.",
        }
    return render(request, 'contact.html', context)

def about(request):
    context={'about_text':"Welcome To About US"}
    return render(request,'about.html',context)