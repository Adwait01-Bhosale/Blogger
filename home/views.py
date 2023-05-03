from django.shortcuts import render, redirect
from datetime import datetime
from home.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from utils.decorator import login_required_message
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from home.forms import ImageForm, Update
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)

class my_dictionary(dict):
  # __init__ function
  def __init__(self):
    self = dict()
 
  # Function to add key:value
  def add(self, key, value):
    self[key] = value
    

def add_values_in_dict(sample_dict, key, list_of_values):
    ''' Append multiple values to a key in 
        the given dictionary '''
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registrations/password_reset.html'
    email_template_name = 'registrations/password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')

@login_required
def newblog(request):

    if request.method == "POST":
        print("entered in IF")
        author_name = request.POST['authorname']
        domain=request.POST['domain']
        title = request.POST['title']
        content = request.POST['content']
        # print(author_name, title, content, datetime.today())
        user=request.user
        ins=BlogData(author=author_name, logged_in_author=request.user ,title=title, domain=domain ,content=content, created_at=datetime.today(), user=request.user)
        ins.save()
    
    return render(request, 'newblog.html')

@login_required
def home(request):
    
    if request.method=="POST":
        print("Entered in IF!!!!!")

        contact_email=request.POST.get('contact_email')
        contact_subject=request.POST.get('contact_subject')
        contact_message=request.POST.get('contact_message')

        print(f"Email: {contact_email}")
        print(f"Subject: {contact_subject}")
        user=request.user
        cont=ContactDetailsData(email=contact_email,subject=contact_subject, message=contact_message, user=user)
        cont.save()
        return redirect('home')
    
    users = Account.objects.filter(is_admin=False).values('fullname', 'id')
    users = list(users)
    
    for user in users:
        if request.user.is_authenticated:
            
            user_name=Account.objects.values_list('fullname')
            
            for names in user_name:
                if str(request.user) == str(names[0]):
                    print(f"The name of the user is: {names[0]}")
            
            # print(request.user)
            content_data = BlogData.objects.order_by('submitted_on').values_list('content')[:4]
            context_blog_data=[]
            
            for i in range (len(content_data)):
                context_blog_data.append(content_data[i])
                
            # print(f"Blogs data is: {context_blog_data}")

            title_data = BlogData.objects.values_list('title')
            context_blog_title=[]
            
            for i in range (len(title_data)):
                context_blog_title.append(title_data[i])
            
            blog_title_dict=my_dictionary()
        
            user['show'] = True

            for i in range(len(context_blog_data)):
                blog_title_dict.add(context_blog_title[i][0], context_blog_data[i][0])

            return render(request, 'home.html', context={'blog_data':blog_title_dict})
        else:
            user['show'] = False
            user['content'] = "Add some Content for the blog!"
    
    if request.user.is_authenticated:
        print("Logged in!!")
        mydata = BlogData.objects.filter(user=request.user).values()
        print(mydata)
    else:
        print("Not logged in!")
        
    return render(request, 'home.html')


@login_required
def dashboard(request):
    
    if request.method=="POST":
        print("Dashboard POST method IF entry")
        name=request.POST.get('name')
        domain=request.POST.get('domain_of_interest')
        dob=request.POST.get('dob')
        college_company=request.POST.get('college_company')

        print("Check -----------------------------")
        
        user=request.user
        profile=profileData(name=name,domain_of_interest=domain, dob=dob, college_company=college_company, user=user)
        profile.save()
        
        
        return render(request,'profile.html')
    else:
        
        if request.user.is_authenticated:
            image_path=""
            users_doi=""
            
            new_list_users=Image.objects.values_list(flat=True)
            
            for new_users in new_list_users:
                user_name=Image.objects.get(id=new_users).user
                users_doi=Account.objects.get(fullname=request.user).domain
                
                if str(request.user) == str(user_name):
                    image_path=Image.objects.get(id=new_users).img
                    break
            
            count=0
            list_of_users=BlogData.objects.values_list(flat=True)
            author_names=[]
            for users in list_of_users:
                user_name=BlogData.objects.get(id=users).user
                author_name=BlogData.objects.get(id=users).author
                author_names.append(author_name)
                if str(user_name)==str(request.user):
                    count+=1

            print(f"List of authors is: {author_names}")
            return render(request,'profile.html', context={'images':"media/"+str(image_path),
                                                           'domain_of_interest':users_doi,
                                                           'count':count})
    
    return render(request, 'profile.html')

@login_required
def upload_image(request):
    try:
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)

            if form.is_valid():
                profile=form.save(commit=False)
                profile.user=request.user
                profile.save()
                return render(request, "home.html", {"form": form}) 
        else:
            form = ImageForm()
    except:
        messages.info(request, 'You can upload image only once!')
    return render(request, "upload_image.html", {"form": form}) 

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })



@login_required
def myblogs(request):
    
    users = Account.objects.filter(is_admin=False).values('fullname', 'id')
    users = list(users)
    
    my_blogs_title_content=my_dictionary()
    author_name=""


    if request.user.is_authenticated:
        
        list_of_users=BlogData.objects.values_list(flat=True)

        
        data_dict={}
        data_list=[]
        
        for users in list_of_users:
            
            user_name=BlogData.objects.get(id=users).user
            
            author_blog_title=BlogData.objects.get(id=users).title
            author_blog_content=BlogData.objects.get(id=users).content
            blog_submittedon=BlogData.objects.get(id=users).submitted_on
            # print(f"Blog submission dates: {blog_submittedon}")
            
            if str(user_name)==str(request.user):
                print("USER IDS ARE: \n")
                print(users)
                print(blog_submittedon)
                author_name=BlogData.objects.get(id=users).author
                my_blogs_title_content.add(author_blog_title,author_blog_content)
                
                data_list.append(author_blog_title)
                data_list.append(author_blog_content)
                data_list.append(blog_submittedon)
                data_dict[users]=data_list

        # print(data_dict.values())
        
        print("---------------------")
        for key, values in data_dict.items():
            for val in values:
                print(val)
        
        # return render(request, "myblogs.html", context={'myblogs_contents':my_blogs_title_content,
        #                                                 'name_of_author':author_name})
        return render(request, "myblogs.html", context={'myblogs_contents':my_blogs_title_content,
                                                        'name_of_author':author_name})
            
    else:
        print("Not logged in!")
    return render(request,"myblogs.html")

@login_required
def update_view(request, id):
    # dictionary for initial data with
    # field names as keys
    print("--------------------")
    context={}
    
    # list_of_users=BlogData.objects.values_list(flat=True)
    # print(list_of_users)
 
    # fetch the object related to passed id
    obj = get_object_or_404(BlogData, id = id)
    
    # pass the object as instance in form
    form = Update(request.POST or None, instance = obj)
 
    users = Account.objects.filter(is_admin=False).values('fullname', 'id')
    users = list(users)
    ids_list=my_dictionary()
    
    count=0
    
    if request.user.is_authenticated:
        list_of_users=BlogData.objects.values_list(flat=True)
        print(f"List of users are: {list_of_users}")
        for users in list_of_users:
            user_name=BlogData.objects.get(id=users).user
            author_blog_title=BlogData.objects.get(id=users).title
            
            if str(user_name)==str(request.user):
                print(f"Count is: {count}")
                print(f"Title for user id {users} is {author_blog_title}")
                
                ids_list.add(users, author_blog_title)
                count+=1
    
    print(f"User ID's if they have published a blog: {ids_list.values()}")
    
    if form.is_valid():
        form.save()
        return render(request, "myblogs.html")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "update_post.html", context)


def delete_post(request, post_id=None):
    post_to_delete=BlogData.objects.get(id=post_id)
    post_to_delete.delete()
    return redirect(request, 'myblogs.html`')