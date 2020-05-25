from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.contrib import messages

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post


class PostListView(LoginRequiredMixin,ListView):
    model = Post
    title='Feed'
    template_name = 'socio/feed.html'  # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    ordering = ['-date_posted']



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


def home(request):
    context = {
        'title':'Home'
    }
    return render(request,'socio/home.html',context)



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
	'title':'Profile'}
	return render(request,'socio/profile.html',context)