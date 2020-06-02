from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post
from .filters import PostFilter
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.contrib import messages

# class PostDetailView(LoginRequiredMixin,DetailView):
#     model = Post
#     def get_context_data(self, *args, **kwargs): 
#         context = super(PostDetailView, self).get_context_data(*args, **kwargs)
#         context["title"] = 'Post Details'
              
#         return context

@login_required    
def post_detail(request,pk):
    post=Post.objects.get(id=pk)
    is_liked=False
    if post.likes.filter(id=request.user.id).exists():
        is_liked=True
    context={
    'title': 'Post Details',
    'object':post,
    'is_liked':is_liked,
    'total_likes':post.likecount()
    }
    return render(request,'socio/post_detail.html',context)


class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'socio/feed.html'
    context_object_name = "posts"
    ordering = ['-date_posted']
    def get_context_data(self, *args, **kwargs): 
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context["title"] = 'Newsfeed'              
        return context



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image','title', 'caption','link']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['image','title', 'caption','link']
    # success_url = '/feed/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/feed/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def delete_user(request):
    context = {
        'title':'Deactivate Account'
    }
    return render(request,'socio/deactivate.html',context)

@login_required
def delete_user_confirm(request):
    context = {}
    if request.user.is_authenticated:
        username = request.user.username
    try:
        u = User.objects.get(username=username)
        u.delete()
        context['msg'] = 'The user is deleted.'       
    except User.DoesNotExist: 
        context['msg'] = 'User does not exist.'
    except Exception as e: 
        context['msg'] = e.message

    messages.success(request,f' {username} account is deleted !')
    return redirect('socio-home')

def signup(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username} !')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request,'socio/signup.html',{'form':form,'title':'Sign up to socio'})

@login_required
def filter_list(request):
    f = PostFilter(request.GET, queryset=Post.objects.all().order_by('-date_posted'))
    return render(request, 'socio/filtered.html', {'filter': f,'title':'Search Post in Socio'})

def home(request):
    context = {
        'title':'Socio Home'
    }
    return render(request,'socio/home.html',context)


@login_required
def dashboard(request):
    logged_in_user = request.user
    logged_in_user_posts = Post.objects.filter(author=logged_in_user).order_by('-date_posted')
    cnt=logged_in_user_posts.count()
    context = {
        'title':'DashBoard',
        'posts': logged_in_user_posts,
        'count':cnt
    }
    return render(request,'socio/dashboard.html',context)

def postlike(request):
    if request.method == 'POST':
        post=get_object_or_404(Post,id=request.POST.get('post_id'))
        is_liked=False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            is_liked=False
        else:
            post.likes.add(request.user)
            is_liked=True

        return HttpResponseRedirect(post.get_absolute_url())


# @login_required
# def feed(request):
#     context = {
#         'posts': Post.objects.all(),
#         'title':'Feed'
#     }
#     return render(request,'socio/feed.html',context)

@login_required
def profile(request):
	if request.method == 'POST':
		uform=UserUpdateForm(request.POST,instance=request.user)
		pform=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
		if uform.is_valid() and pform.is_valid():
			uform.save()
			pform.save()
	else:
		uform=UserUpdateForm(instance=request.user)
		pform=ProfileUpdateForm(instance=request.user.profile)
	context= {
	'uform':uform,
	'pform':pform,
	'title':'Update Profile'}
	return render(request,'socio/profile.html',context)