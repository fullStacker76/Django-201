# from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render

from  .models import Post
from followers.models import Follower

# Create your views here.

class HomePage(TemplateView):
    http_method_names = ["get"]
    template_name = "feed/homepage.html"
    model = Post
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            following = list(Follower.objects.filter(followed_by=self.request.user).values_list("following", flat=True))
            if not following:
                posts = Post.objects.all().order_by("-id")[0:30]
            else:
                context["posts_to_follow"] = Post.objects.filter(author__in=following).order_by("-id")[0:60]                    
                posts = Post.objects.exclude(author__in=following).order_by("-id")[0:60]               
        else:
            posts = Post.objects.all().order_by("-id")[0:30]
            
        context["posts"] = posts
        return context
    
class PostDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "feed/detail.html"
    model = Post
    context_object_name = "post"
    
class CreateNewPost(CreateView, LoginRequiredMixin):
    http_method = ["post"]
    model = Post
    template_name = "feed/create.html"
    fields = ["text"]
    success_url = "/"
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user 
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        post = Post.objects.create(
            text = request.POST.get("text"),
            author = request.user,
        )
        messages.add_message(self.request, messages.SUCCESS, "New Message Posted")
        
        return render(
            request,
            "includes/post.html",
            {
                "post": post,
                "show_detail_link": True,    
            },
            content_type="application/html"
        )

class PostUpdateView(UpdateView, LoginRequiredMixin):
    http_method_names = ["get", "post"]
    model = Post    
    fields = ["text"]
    success_url = "/"
    
    def dispatch(self, request, *args, **kwargs):       
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):         
        messages.add_message(self.request, messages.SUCCESS, "Post Updated")
        return super().form_valid(form)
            

class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = "feed/delete.html"    
    success_url = "/"
    
    def dispatch(self, request, *args, **kwargs):       
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):         
        messages.add_message(self.request, messages.SUCCESS, "Message Deleted")
        return super().form_valid(form)