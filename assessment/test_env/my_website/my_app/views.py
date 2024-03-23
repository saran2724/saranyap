from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,likePost,Followers,Comment
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
# Create your views here.

def home(request):
    return render(request,'website.html')
def index(request):
    post = Post.objects.order_by('-created_at')
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    context = {
        'post': post,
        'profile': profile,
    }
    return render(request,'index.html',context)

def home_post(request,id):
    post=Post.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    context={
        'post':post,
        'profile':profile
    }
    return render(request, 'index.html',context)
def signup(request):
    try:
        if request.method=="POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            my_user=User.objects.create_user(name,email,password)
            my_user.save()
            user_model=User.objects.get(username=name)
            user_model.save()
            new_profile=Profile.objects.create_user(user=user_model,id_user=user_model.id)
            new_profile.save()
            if my_user is not None:
                auth_login(request,my_user)
                return redirect('/')
            return redirect('/')
    except:
        invalid="User Already exists"
        return render(request,'signup.html',{'invalid':invalid})
    return render(request, 'signup.html')

        

def login_view(request):
 
    if request.method == 'POST':
        name=request.POST.get('name')
        password=request.POST.get('password')
        # print(name,password)
        user=authenticate(request,username=name,password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        
 
        invalid="Invalid Credentials"
        return render(request, 'login.html',{'invalid':invalid})
               
    return render(request, 'login.html')
def logout(request):
    return redirect('/login')
@login_required(login_url='/login')
def upload_view(request):
    if request.method == 'POST':
        user = request.user
        print("user",user)
        image = request.FILES.get('image_upload')
        print("image",image)
        caption = request.POST['caption']
       

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')
# def like_post(request, id):
#     if request.method == 'GET':
#         username = request.user.username
#         post = get_object_or_404(Post, id=id)
#         likes = likePost.objects.filter(post_id=id)
#         liked_by_users = [like.username for like in likes]
#         context = {
#             'pos': post,
#             'liked_by_users': liked_by_users
#         }
        
#         return render(request, 'index.html', context)
def like_post(request,id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post, id=id)

        like_filter = likePost.objects.filter(post_id=id, username=username).first()
        print("like_filter",like_filter)

        if like_filter is None:
            new_like = likePost.objects.create(post_id=id, username=username)
            post.no_of_likes = post.no_of_likes + 1
        else:
            like_filter.delete()
            post.no_of_likes = max(0,post.no_of_likes - 1)
        liked_users_queryset = likePost.objects.filter(post_id=id).values_list('username', flat=True)
        liked_users = list(liked_users_queryset)
        print("liked_users",liked_users)
        request.session['liked_users'] = liked_users

        post.save()

      
        print(post.id)
        like_user = your_view(request)

        print("like_user",like_user)
        
        # return redirect('',context)
        # return render(request,'index.html',context)
        return HttpResponseRedirect(reverse('index') + '?liked_users=' + ','.join(liked_users))
def your_view(request):
    liked_users = request.session.get('liked_users', [])
    print("liked_users",liked_users)
    # context={'liked_users':liked_users}
    # print("context",context)
    return{'liked_users':liked_users}
    # return render(request,'index.html',context)
      
def Comment_view(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        print("comment_text",comment_text)
        post_id = request.POST.get('post_id') 
        print("post_id",post_id) 
        post = get_object_or_404(Post,pk=post_id)
        print("post",post) 
        if comment_text:
            comment = Comment.objects.create(text=comment_text, post=post)
            print("hello", comment)
            return redirect('index')
    return render(request, 'comment.html')
    #         return JsonResponse({'status': 'success', 'comment_text': comment.text, 'username': comment.user})
    #     else:
    #         return JsonResponse({'status': 'error', 'message': 'Comment text is empty'})
    # else:
    #     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
def profile(request,username):
    user = get_object_or_404(User, username=username)
    user_object = User.objects.get(username=username)
    print(user_object)
    profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.get(user=user_object)
    # user_posts = Post.objects.filter(user=username).order_by('-created_at')
    # print("user_posts",user_posts)
    # user_post_length = len(user_posts)

    follower = request.user.username
    user = username
    
    if Followers.objects.filter(follower=follower, user=user).first():
        follow_unfollow = 'Unfollow'
    else:
        follow_unfollow = 'Follow'

    user_followers = len(Followers.objects.filter(user=username))
    user_following = len(Followers.objects.filter(follower=username))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        # 'user_posts': user_posts,
        # 'user_post_length': user_post_length,
        'profile': profile,
        'follow_unfollow':follow_unfollow,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    
    
    if request.user.username == username:
        if request.method == 'POST':
            if request.FILES.get('image') == None:
                image = user_profile.profileimg
                bio = request.POST['bio']
                location = request.POST['location']

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()
            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                bio = request.POST['bio']
                location = request.POST['location']

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()
                

            return redirect('/profile/'+username)
        else:
            return render(request, 'profile.html', context)
    return render(request, 'profile.html', context)
  