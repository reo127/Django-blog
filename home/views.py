from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



# Create your views here.

def home(request):
    # Feach top three post base on number os views
    popular = Post.objects.all()
    # print(popular)
    params = {'popular':popular}
    return render(request, 'home/home.html', params)

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        contect = request.POST['content']

        if len(name)<2 or len(email)<3 or len(phone)<11 or len(contect)<4:
            messages.error(request, "Place fill the form currectly")
        else:
            contact = Contact(name=name, email=email, phone=phone, contect=contect)
            contact.save()
            messages.success(request, "Your massage has been send")

    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')


def search(request):
    query=request.GET['query']
    if len(query) > 73:
        allPosts = Post.objects.none()
    else:
        allPoststitle= Post.objects.filter(title__icontains=query)  
        allPostscontect= Post.objects.filter(contect__icontains=query)
        allPosts = allPoststitle.union(allPostscontect)

    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
  
    params={'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params)


def HandleSignup(request):
    if request.method == 'POST':
        # Get the POST peramiters 
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # Cheacks for errorneous inputs
        # Username should be 20 charecters
        if len(username) > 20:
            messages.error(request, 'Your username must be under 20 charerckter')
            return redirect('/')

        # username should be Alfanumarick
        if not username.isalnum():
            messages.error(request, 'Your username should containt numbers and leaters')
            return redirect('/')
        
        # password should be match
        if pass1 != pass2:
            messages.error(request, 'Password do not match')
            return redirect('/')

        # Creat User
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('/')

    else:
      return HttpResponse('404 Not Found ')


def HandleLogin(request):
    if request.method == 'POST':
        # Get the POST peramiters 
        username = request.POST['loginusername']
        password = request.POST['loginpassword']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User Successfuly Login ')
            return redirect('/')
        else:
            messages.error(request, 'Invailed Creadincials, Place try agian')
            return redirect('/')

    return HttpResponse('<center><b><h1>404 Page Not Found</h1></b></center>')

def HandleLogout(request):
    logout(request)
    messages.success(request, 'User Successfuly Loguot')
    return redirect('/')




        

       

