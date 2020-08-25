from django.shortcuts import render,get_object_or_404 ,redirect
from .models import Category,Post,Comment, UserExtended
from django.contrib.auth.models import User

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import date
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse
 
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login


from django.views.decorators.csrf import csrf_protect
import datetime

today = date.today()

def calculate_age(born):
    daysLeft = today - born
    print(daysLeft)

    years = ((daysLeft.total_seconds())/(365.242*24*3600))
    yearsInt=int(years)

    months=(years-yearsInt)*12
    monthsInt=int(months)

    days=(months-monthsInt)*(365.242/12)
    daysInt=int(days)
    s = 'You are {0:d} years, {1:d}  months, {2:d}  days old.'.format(yearsInt,monthsInt,daysInt)
    age = {
        "year": yearsInt,
        "month": monthsInt,
        "day":daysInt
    }
    return age




# Create your views here.
def index(request):
    categories = Category.objects.all()
    post5 = Post.objects.filter(status=1).order_by('-updated_on')[0:5]
    post = Post.objects.all()
    paginator = Paginator(post, 10)  # 10 posts in each page
    page_number = request.GET.get('page')
    post_list = paginator.get_page(page_number)


    
    print(type(post_list))
    context = {
        'posts': post5,
        'categories':categories,
        "post_list":post_list
       
    }
    return render(request, "article/index.html", context)

def category(request, category):
    cat = Category.objects.filter(category_slug=category).first()
    posts = Post.objects.filter(category=cat.id)
    categories = Category.objects.all()
    paginator = Paginator(posts, 10)  # 10 posts in each page
    page_number = request.GET.get('page')
    post_list = paginator.get_page(page_number)
    post5 = Post.objects.filter(status=1).order_by('-updated_on')[0:3]
    
    
    context = {
        "posts":post5,
        'categories':categories,
        "cat"   : cat,
        "post_list":post_list
        
    }

    return render(request, "article/category.html", context)





@csrf_protect
def singlePost(request,category, post):
    cat = Category.objects.filter(category_slug=category).first()
    categories = Category.objects.all() 
    post = get_object_or_404(Post, slug=post,category=cat.id)
    comments = post.comments.filter(active=True)
    post3 = Post.objects.filter(status=1).order_by('-updated_on')[0:3]
    
    #birthday = calculate_age(user_bday)
    context = {
        "posts":post,
        "comments": comments,
        "categories":categories,
        "post3" :post3
        
        
    }
    
    if request.method == 'POST':
        
       
        current = request.user
        current_user = UserExtended.objects.filter(user=current.id).first()
        
        
        
        try:
            
            new_comment = Comment.objects.create(
                name = current_user,
                post = post,
                body = request.POST.get("commentbody"),
                
            )
            name11 = new_comment.name.user.first_name + " "+ new_comment.name.user.last_name
            
            comment_data = {
                "avatar": new_comment.name.avatar.url,
                "name"  : name11,
                "body"  : new_comment.body,
                "time"  : new_comment.created_on.strftime("%B %-d, %Y"),
                "msg"   :"Success",
                "status_code": 200
                
            }         
            response = JsonResponse(comment_data, safe=False)
            
            
            return response
        except:
            response = JsonResponse({"msg":"Failed, try again", "status_code": 404}, safe=False)   
            return response
    
    
    return render(request, "article/single.html", context)

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method == 'POST':
        usr = request.POST.get("usr")
        pas = request.POST.get("pas")
        try:
        
            user = authenticate(request, username=usr, password=pas)
            if user is not None:
                auth_login(request, user)
                login_data = {
                    "msg": "success",
                    "status_code":200}        
                response = JsonResponse(login_data, safe=False)
                return response
                
            else:
                response = JsonResponse({"msg":"Wrong Credentials","status_code":503}, safe=False)   
                return response
            
        
            
            
            
        except:
            response = JsonResponse({"msg":"Something went wrong","status_code":503}, safe=False)   
            return response

    return render(request, "article/login.html")

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method == 'POST':
        
        username = request.POST.get("username")
        print(username)
        
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        birthdate = request.POST.get("birthdate")
        avatar = request.FILES.get("avatar")
        if User.objects.filter(username=username).exists():
            response = JsonResponse({"msg":"Username Already exists, try different username"}, safe=False)   
            return response
        if password2 != password1:
            response = JsonResponse({"msg":"Two password don't match!"}, safe=False)   
            return response

        try:
            user = User.objects.create_user(username, email, password2)
            user.first_name = fname
            user.last_name = lname
            user.save()
            
            ext = UserExtended(user = user, gender= gender, about= "hello",birthday = birthdate, avatar= avatar)
            ext.save()
            auth_login(request, user)
            response = JsonResponse({"msg":"Registration Succesfull, Please login now"}, safe=False)   
            return response
        
        except:
            response = JsonResponse({"msg":"Registration failed, Something went wrong"}, safe=False)   
            return response
       
        

    return render(request,"article/register.html")

def logout_view(request):
    logout(request)
    return redirect('login')

def createPost(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    categories = Category.objects.all()

    if request.method == 'POST':
        current = request.user
        current_user = UserExtended.objects.filter(user=current.id).first()

        title = request.POST.get("title")
        slug = request.POST.get("slug")
        category = request.POST.get("category")
        content = request.POST.get("content")
        thumb = request.FILES.get("thumbnail")

        cat = Category.objects.filter(category_slug=category).first()
        try:
            new_post = Post.objects.create(
                title = title,
                slug = slug,
                author = current_user,
                thumbnail= thumb,
                content = content,
                category = cat,
            )
            return redirect('singlePost',category = new_post.category.category_slug, post= new_post.slug)
        except:
            print("Something Wrong!!!!!")
        



    context = {
        "categories" : categories,

    }
    return render(request,"article/addPost.html", context)

