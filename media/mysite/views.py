from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from app.models import Categories,Course,Levels,Post,Author,Assignment,Score,Course,Submission,Enrollment
from django.template.loader import render_to_string
from ckeditor.fields import RichTextField
from app.forms import PostForm
def base(request):
    return render(request,'base.html')
def logoutpage(request):
    logout(request)
    return render(request,'main/index.html')
def contact(request):
    category = Categories.objects.all ()
    course = Course.objects.all ()
    if request.method=="POST":
        name = request.object.get(name)
        email = request.object.get ( email)
        message = request.object.get(message)
        obj =Contact(name=name,email=email,)



        print("dsa")
    return render(request,'main/contact.html',{"category":category,"course":course})
def aboutus(request):
    category = Categories.objects.all ()
    course = Course.objects.all ()
    return render(request,'main/aboutus.html',{"category":category,"course":course})
def home(request):
    category = Categories.objects.all()
    course = Course.objects.all()
    teacher = Author.objects.all()
    print(teacher)
    return render(request,'main/index.html',{"category":category,"course":course,"teacher":teacher})
def course(request):
    category = Categories.objects.all()
    levels = Levels.objects.all()
    course = Course.objects.all()


    return render(request,'main/single_course.html',{'categories':category,'levels':levels,"course":course,"category":category})
def filter_courses(request):
    category = request.GET.getlist('category[]')
    levels = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print(price)
    if category :
        course = Course.objects.filter ( category__id__in=category).order_by ( '-id' )
    elif levels:
        course = Course.objects.filter(level__id__in=levels).order_by ( '-id' )


    else:
        course = Course.objects.all()
    t = render_to_string( 'ajax/course.html',{'course':course} )
    return JsonResponse ( {'data': t} )
def assignment(request):
    if request.method == "POST":
              link = request.POST.get('assignment')
              user =  request.user
              print(link)
              print(user)
              if (link is not None):

                  project = Assignments(link=link,user_details=user)
                  project.save()
                  messages.success ( request, 'Assignment  successfully submitted' )
                  print("Suuccess asssignment")
                  return redirect("home")
    return None

def loginpage(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(username=username, password=password)

        if user is not None:
            print("correct")
            login(request,user)
            messages.success(request,"Successfully login")
            return redirect('home')
        else:

            messages.warning(request,'Invalid user')
            return redirect('login')

    return render(request,'regestration/login.html')
def register(request):
    if request.method=='POST':
        username = request.POST.get("username")
        email = request.POST.get ( "email" )
        password = request.POST.get ( "password" )

    #     check
        if User.objects.filter(email=email).exists():
            messages.warning(request,'Email already exists')
            return redirect ('register')
        if User.objects.filter(username=username).exists():
            messages.warning ( request, 'Username already exists' )
            return redirect ( 'register' )

        user = User(username = username,email=email)
        user.set_password(password)
        user.save()
        messages.success ( request, 'Register successfully' )
        return redirect ('register')
    return render(request,'regestration/register.html')
def search_courses(request):
    query = request.GET['query']
    category = Categories.objects.all ()
    course = Course.objects.filter (title__icontains=query)

    return render(request,'search.html',{'category':category,'course':course})
def profile(request):
    return render(request,'regestration/profile.html')
def game(request):
    return render(request,'course/game.html')
def game2(request):
    return render ( request, 'course/game2.html' )
def treasure_hunt(request):
    return render ( request, 'course/treasure_hunt.html' )
def profile_update(request):

        if request.method == "POST":
            username = request.POST.get ( 'username' )
            first_name = request.POST.get ( 'first_name' )
            last_name = request.POST.get ( 'last_name' )
            email = request.POST.get ( 'email' )
            password = request.POST.get ( 'password' )
            user_id = request.user.id
            print(username,first_name,last_name)
            user = User.objects.get ( id=user_id )
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email

            if password != None and password != "":
                user.set_password ( password )
            user.save ()

            messages.success( request, 'Profile Are Successfully Updated. ' )
            print("UPdatess")
            return redirect ( 'profile' )

        return redirect ( 'home' )
def course_detalis(request,slug):
    course = Course.objects.filter(slug=slug)
    obj = Enrollment.objects.filter(user=request.user,course=course[0]).exists()
    print(obj,course[0])
    assign_discuss=False
    if obj:

        assign_discuss=True

    if course.exists():
        course = course.first()
    else:
        return redirect('error')
    return render (request,'course/course_detail.html',{'course':course,"assign_discuss":assign_discuss})
def page_not_found(request):
    return render(request,'error/404.html')
def discuss(request,slug):
    course = Course.objects.filter ( slug=slug )[0]
    queries = Post.objects.filter(course=course) 
    form = PostForm
    if(request.method=="POST"):
        form = PostForm ( request.POST )
        user= request.user
        course=Course.objects.filter(slug=slug)
        parent  = request.POST.get('parent')
        print (parent,"parent id ")


        if (form.is_valid()):
            comments = form.cleaned_data['comments']
        if (parent==""):
             print("NULLL")
             Post.objects.create(name=user,comments=comments,course=course[0])
        else:
             parentdetail = Post.objects.filter(id=parent)
             print(parentdetail,"parentdetail")
             Post.objects.create(name=user,comments=comments,course=course[0],parent=parentdetail[0])
    return render(request,'course/discuss.html',{"form":form,'slug':slug,"queries":queries})
def assignment(request,slug):
    course = Course.objects.filter ( slug=slug )[0]
    assignment = Assignment.objects.filter(course = course)[0]
    enrolled = Enrollment.objects.filter(user = request.user,course=course).exists()
    if enrolled:
      score= Score.objects.filter(user_detail=request.user,assignment=assignment,course=course).exists()
      if score:
        grad = Score.objects.get(user_detail=request.user,assignment=assignment,course=course)
        score=grad.grades
      else:
        score="Assignment not submitted"
    if request.method=="POST":
        user = request.user
        link = request.POST.get('assignment')
        obj = Submission(user=user,course=course,link = link)
        obj.save()


    return render(request,'course/assignment.html',{"assignment":assignment,'score':score})
def enrollment(request,slug):
    if request.method=="POST":
        course = Course.objects.filter ( slug=slug )[0]
        user = request.user
        print(user)
        print(course)
        student = Enrollment.objects.filter(user=user,course = course).exists()
        if student:
            pass
        else:
             stu = Enrollment ( user=user, course=course )
             stu.save()
             return redirect ( 'home' )
    return  redirect('home')
