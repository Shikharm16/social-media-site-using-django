from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post,Comment
from django.db.models import Count
from django.utils.datastructures import MultiValueDictKeyError
from .filters import PostFilter
import pandas as pd
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.contrib import messages
# from notify.signals import notify
# class PostDetailView(LoginRequiredMixin,DetailView):
#     model = Post
#     def get_context_data(self, *args, **kwargs): 
#         context = super(PostDetailView, self).get_context_data(*args, **kwargs)
#         context["title"] = 'Post Details'
#         return context

@login_required    
def post_detail(request,pk):
    post=Post.objects.get(id=pk)
    ied=pk
    comments=Comment.objects.filter(post=post).order_by("-pk")

    is_liked=False
    if post.likes.filter(id=request.user.id).exists():
        is_liked=True
    else:
        is_liked=False

    is_favorite=False
    if post.favorites.filter(id=request.user.id).exists():
        is_favorite=True
    else:
        is_favorite=False

    if request.method == 'POST':
        cf=CommentForm(request.POST or None)
        if cf.is_valid():
            content=request.POST.get('content')
            comment=Comment.objects.create(post=post,user=request.user,content=content)
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        cf=CommentForm()

    context={
    'title': 'Post Details',
    'comments':comments,
    'ied':ied,
    'object':post,
    'is_favorite': is_favorite,
    'is_liked':is_liked,
    'total_likes':post.likecount(),
    'comment_form':cf
    }
    return render(request,'socio/post_detail.html',context)

@login_required
def favorite(request,id):
    post=get_object_or_404(Post,id=id)
    if post.favorites.filter(id=request.user.id).exists():
        messages.success(request,f'bookmark removed !')
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
        messages.success(request,f'Post Saved! You can check it out in your Bookmarks.')
    return HttpResponseRedirect(post.get_absolute_url())

@login_required
def favorite_list(request):
    user=request.user
    post=user.favorites.all()
    context={
    'post':post,
    'title': 'Bookmarks'
    }
    return render(request,'socio/bookmark.html',context)

@login_required
def postlike(request):
    if request.method == 'POST':
        post=get_object_or_404(Post,id=request.POST.get('post_id'))
        is_liked=False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            is_liked=False
        else:
            post.likes.add(request.user)
            # notify.send(request.user, recipient=post.author, actor=request.user,
            #     verb='liked your post', nf_type='liked_post')
            is_liked=True

        return HttpResponseRedirect(post.get_absolute_url())

@login_required
def deletecomment(request,id):
    comment=get_object_or_404(Comment,id=id)
    comment.delete()
    messages.success(request,f'Comment deleted!')
    return redirect(comment.post.get_absolute_url())

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
    success_url = '/dashboard'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['image','title', 'caption','link']
    success_url = '/dashboard'

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
    success_url = '/dashboard'

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
def document(request):
    if request.method == 'POST':
        try:
            f=request.FILES['file']
            messages.success(request,f'file uploaded')
            #print("Uploaded")

            data_xls = pd.read_excel(f)
            df=data_xls[['Name of Hospital ','Sex','DATE OF COLLECT SAMPLE','Age']]

            if len(df['Sex'].unique()) == 2:
                msg1="Valid Sex"

            if 'DATE OF COLLECT SAMPLE' in df:
                try:
                    pd.to_datetime(df['DATE OF COLLECT SAMPLE'], format='%d/%m/%Y')
                except:
                    msg2="incorrect date format"

            if 'Age' in df:
                if df['Age'].between(0,110).all():
                    msg3="Valid Age"
                else:
                    msg3="Invalid age"

            data={'Sex': msg1,
            'Date':msg2,
            'Age':msg3
            }
            print(data)
            context = {
                'title':'docxx',
                'data':data
            }
                                
            return render(request,'socio/fileupload.html',context)

        except MultiValueDictKeyError:
            messages.warning(request,f'No file selected! Upload again!')
    context = {
        'title':'docxx'
    }
    return render(request,'socio/fileupload.html',context)

@login_required
def trending(request):
    post=Post.objects.annotate(like_count=Count('likes')).order_by('-like_count','-date_posted')
    context = {
        'title':'Trending',
        'posts':post,
    }
    return render(request,'socio/trending.html',context)

@login_required
def dashboard(request):
    logged_in_user = request.user
    logged_in_user_posts = Post.objects.filter(author=logged_in_user).order_by('-date_posted')
    cnt=logged_in_user_posts.count()
    context = {
        'title':'DashBoard',
        'posts': logged_in_user_posts,
        'count': cnt
    }
    return render(request,'socio/dashboard.html',context)

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

