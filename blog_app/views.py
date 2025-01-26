from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Posts,Message
from .forms import Add_Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm, ProfileForm

# Create your views here.
@login_required(login_url="/login/")
def home(request):
    posts = Posts.objects.all()
    context = {
        'posts': posts
    }
    return render(request,'home.html',context)
@login_required(login_url="/login/")
def add(request):
    if request.method == 'POST':
        form = Add_Post(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request,'Your Post is successfully Uploaded!!!!')
            return redirect('/')
    else:
        form = Add_Post()
    return render(request, 'add_post.html',{'form':form})

@login_required(login_url="/login/")
def posts_full(request,pk):
    post = Posts.objects.get(id=pk)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        comment = Message.objects.create(user=request.user,
                                        post=post,
                                        body=request.POST.get('content'))
        messages.success(request,"Comment is added Successfully !!!!")
        return redirect('full-post',pk=post.id)
    
    
    context={'posts':post,'comments':comments}
    return render(request,'posts.html',context)



def logout_page(request):
    logout(request)
    return redirect('/login/')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username,password=password)
            if user is None:
                messages.info(request,'Invalid Password')
                return redirect('/login/')
            else:
                login(request,user)
                messages.success(request,'Login successful')
                return redirect('/')
        
        else:
            messages.error(request,"Invalid Username")
            return redirect('/login/')
        
        
    return render(request,'login.html')


def register(request):
    if request.method == "POST":
        # first_name =  request.POST.get('first_name')
        # last_name =  request.POST.get('last_name')
        username =  request.POST.get('username')
        email =  request.POST.get('email')
        password =  request.POST.get('password')
        
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username already taken')
            return redirect('/register/')
        user = User.objects.create_user(username=username,email=email)
        user.set_password(password) #password converted into hashes 
        user.save()
        messages.success(request,f'Your account successfully created at Blog site')
        return redirect('/')
        
    return render(request,'register.html')



@login_required(login_url="/login/")
def deletecomment(request,pk):
    comment = Message.objects.get(id=pk)
    if request.user != comment.user:
        # return HttpResponse('Your are not allowed')
        messages.error(request, "You are not allowed to delete this comment.")
        return redirect('full-post', pk=comment.post.id)
    if request.method == "POST":
        comment.delete()
        messages.success(request,"Comment is deleted Successfully !!!!")
    return redirect('full-post',pk=comment.post.id)
    
    
def user_profile(request,pk):
    # user = User.objects.get(id=pk)
    user = get_object_or_404(User, id=pk)
    posts = user.posts_set.all()
    posts = Posts.objects.filter(user=user)
    context = {'user':user,'posts':posts}
    return render(request,'profile.html',context)

