from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import UserProfileMultiForm
from feed.models import Post
from followers.models import Follower

# Create your views here.

class ProfileDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers'] = Follower.objects.filter(following=user).count()
        
        if self.request.user.is_authenticated:
            context["you_follow"] = Follower.objects.filter(following=user, followed_by=self.request.user).exists()
                
        return context
    
class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = User
    template_name = "profiles/update.html"
    form_class = UserProfileMultiForm        
    context_object_name = 'user'   
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'user': self.object,
            'profile': self.object.profile,
        })
        messages.add_message(self.request, messages.SUCCESS, "Profile Updated")        
        return kwargs
    
class ProfileDeleteView(DeleteView, LoginRequiredMixin):
    model= User
    template_name = "profiles/delete.html"
    success_url = "/"
    
    def form_valid(self, form):
       messages.add_message(self.request, messages.SUCCESS, "Profile Deleted")
       return super().form_valid(form)
    
class FollowerView(View, LoginRequiredMixin):
    http_method_names = ["post"]  
    
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        
        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing Data")
        
        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("User Does Not Exist")
        
        if data['action'] == 'follow':
            #follow
            follower, created = Follower.objects.get_or_create(
                followed_by = request.user,
                following = other_user,
            )
        else:
            #unfollow
            try:
                follower = Follower.objects.get(
                    followed_by = request.user,
                    following = other_user
                )
            except Follower.DoesNotExist:
                follower = None
                
            if follower:
                follower.delete()
        
        return JsonResponse({
            'success': True,
            'wording': "Unfollow" if data['action'] == "follow" else "Follow"
            })  