from django.shortcuts import render,HttpResponseRedirect,reverse,redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Post,Comment
from .forms import addComment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)
@login_required
def PostLike(request):
    id=request.POST.get('id')
    post=Post.objects.filter(id=id)[0]
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    if request.is_ajax():
        html = render_to_string('blog/likes.html',{"post":post}, request=request)
        print("inside")
        return JsonResponse({'form': html})
    return HttpResponseRedirect(post.get_absolute_url())

@login_required
def Delete_comment(request):
    id=request.POST.get('id')
    pid=request.POST.get('pid')
    post=Post.objects.filter(id=pid)[0]
    print(request.POST)
    Comment.objects.filter(id=id).delete()
    #we need to go to post
    if request.is_ajax():
            html = render_to_string('blog/comments.html',{"post":post,"form":addComment}, request=request)
            return JsonResponse({'form': html})
    return HttpResponseRedirect(reverse('post-details',kwargs= {'pk':int(request.POST['next'])}))


class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_created']
    paginate_by=2

class OtherPostListView(ListView):
    model=Post
    template_name='user/other_user.html'
    context_object_name='posts'
    ordering=['-date_created']

class PostDetailView( FormMixin,DetailView):
    model=Post
    ordering=['date_created']
    form_class=addComment
    def get_success_url(self):
        return reverse('post-details', kwargs={'pk': self.object.id})
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            x=self.form_valid(form)
            if self.request.is_ajax():
                html = render_to_string('blog/comments.html',{"post":self.object,"form":addComment}, request=request)
                return JsonResponse({'form': html})
            return x
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        form.instance.author=self.request.user
        form.save()
        post=self.get_object()
        post.comments.add(form.instance)
        return super(PostDetailView, self).form_valid(form)

    

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        return self.request.user==post.author

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        post=self.get_object()
        return self.request.user==post.author

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})