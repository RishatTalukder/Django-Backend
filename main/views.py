from django.shortcuts import render,redirect
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.
def home(request):
    return render(request, "main/home.html")

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    context = {"topics": topics}
    return render(request, "main/topics.html", context)

@login_required
def topic(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    if topic.owner != request.user:
        raise Http404
    
    context = {'topic':topic, 'entries':entries}
    return render(request,'main/topic.html',context)

@login_required
def new_topic(request):
    if request.method != "POST":
        form = TopicForm()

    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('main:topics')

    context = {'form':form}
    return render(request,'main/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != "POST":
        form = EntryForm()

    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry =  form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()

            return redirect('main:topic',topic_id = topic_id)
    
    context = {'form':form,'topic':topic}
    return render(request,'main/new_entry.html',context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm(instance=entry)
    
    else:
        form = EntryForm(instance=entry,data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('main:topic',topic_id=topic.id)

    
    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'main/edit_entry.html',context)