
from users.forms import EmailSignupForm
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render # to insert template and render it
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .forms import CommentForm





# def blogs(request):
#     context = {'posts':Post.objects.all()} #grab all posts from the post model (DB) and put them in a variable
#     return render(request, 'blog/blogs.html', context) # first request then, 'directory/template' , accessible data

class PostListView(ListView):
    model = Post #this is all we need to create a Listview
    template_name = 'blog/blogs.html' # set new template to look for
    context_object_name = 'posts' #tell what should be used as
    ordering = ['-date_posted']
    paginate_by = 5
    # ordering = Post.objects.annotate(Count("likes")).values("likes__count").order_by()
    
class UserPostListView(ListView):
    model = Post #this is all we need to create a Listview
    template_name = 'blog/user_post.html' # set new template to look for
    context_object_name = 'posts' #tell what should be used as
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    

class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView, self).get_context_data(**kwargs)
        
    #     getidofpost = get_object_or_404(Post, id=self.kwargs['pk'])
    #     liked = False
    #     if getidofpost.likes.filter(id=self.request.user.id).exists():
    #         liked = True

    #     context['liked'] = liked
    #     return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user # add the data necessary to form post 
        form.instance.post = self.object
        form.save()
        return super(PostDetailView, self).form_valid(form)

        


class PostCreateView(LoginRequiredMixin, CreateView): #similar to login required
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user #set loggedin user to author before validating since each post needs a valid author
        return super().form_valid(form) #super runs the original function as we are overriding it

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #similar to login required
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user #set loggedin user to author before validating since each post needs a valid author
        return super().form_valid(form) #super runs the original function as we are overriding it

    def test_func(self): # test whether user is also the author of the object
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): #similar to login required
    model = Post
    fields = ['title', 'content']
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #similar to login required
    model = Comment
    fields = ['content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user #set loggedin user to author before validating since each post needs a valid author
        return super().form_valid(form) #super runs the original function as we are overriding it

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): #similar to login required
    model = Comment
    fields = ['content']
    success_url = '/'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False



@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user) #we are saving a like from a user
        liked = True
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



class AboutListView(ListView):
    model = Profile #this is all we need to create a Listview
    template_name = 'blog/about.html' # set new template to look for
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profilesenne'] = Profile.objects.get(user_id=User.objects.get(username='Senner').id)
        #context['profilereinthaler'] = Profile.objects.get(user_id=2)
        return context
     #value for the title

def home(request):
    form = EmailSignupForm
    return render(request, 'blog/home.html', {'form': form})

def archive(request):
    return render(request, 'blog/archive.html', {'title': 'Archive'})

def impressum(request):
    return render(request, 'blog/impressum.html', {'title': 'Impressum'})

def comingsoon(request):
    return render(request, 'blog/coming-soon.html', {'title': 'Coming-Soon'})

