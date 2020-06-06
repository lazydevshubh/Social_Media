from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect,reverse
from .forms import UserRegistrationForm,UserUpdationForm,ProfileUpdationForm,messageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView
from blog.models import Post
from .models import Message
from django.core.paginator import Paginator

def register(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get("username")
            messages.success(request,"Congratulations on creating new account,You may Login now "+str(username))
            return redirect("login")

    else:
        form=UserRegistrationForm()
    return render(request,"users/register.html",{'form':form})

class OtherPostListView(ListView):
    model=Post
    template_name='users/other_user.html'
    context_object_name='posts'
    ordering=['-date_created']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super(OtherPostListView, self).get_context_data(**kwargs)
        context['users'] = User.objects.get(username=self.kwargs['username'])
        return context

def others(request,username):
    if request.user.username==username:
        return redirect("profile")
    else:
        user=User.objects.get(username=username)
        context={'users':user}
        return render(request,"users/other_user.html",context)

@login_required
def messages(request,id):
    if request.method=="GET":
        messages=Message.objects.all().order_by('-date_sent')
        data=[]
        for message in messages:
            if (message.sender.id==id and message.reciever.id==request.user.id) or (message.reciever.id==id and message.sender.id==request.user.id):
                data.append(message)
        to=User.objects.filter(id=id)[0].username
        form=messageForm()
        context={"Usermessages":data,"to":to,"form":form}
        return render(request,"users/message.html",context)
    elif request.method=="POST":
        message=messageForm(request.POST)
        if message.is_valid():
            mess=message.save(commit=False)
            mess.sender=request.user
            mess.reciever=User.objects.filter(id=id)[0]
            mess.save()
            return HttpResponseRedirect(reverse('messages',kwargs= {'id':id}))
        else:
            print("invalid")


@login_required
def profile(request):
    if request.method=="POST":
        u_form=UserUpdationForm(request.POST,instance=request.user)
        p_form=ProfileUpdationForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,"Profile Updated!")
            return redirect("profile")
        else:
            messages.error(request,"Wrong details")
            return redirect("profile")
    else:
        u_form=UserUpdationForm(instance=request.user)
        p_form=ProfileUpdationForm(instance=request.user.profile)

        context={'u_form':u_form,'p_form':p_form}
        return render(request,"users/profile.html",context) 