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
from home.forms import ImageForm

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
        ins=BlogData(author=author_name, title=title, domain=domain ,content=content, created_at=datetime.today(), user=request.user)
        ins.save()
    
    return render(request, 'newblog.html')

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
            
            content_author_dict={}
            
            # for i in range(len(title_data)):
            #     content_blog_authors=BlogData.objects.get(content=context_blog_data[i][0]).author
            #     print(f"Name of the author is: {content_blog_authors}")
                
            #     author_blog_content=BlogData.objects.get(author=content_blog_authors).content
                
            #     print("-------------------------")
            #     print(author_blog_content)
                # content_blog_title=BlogData.objects.get(content=author_blog_content[i]).title
                # print("-------------------")
                # print(f"This is the title of respective blog content: {content_blog_title}")
                # content_author_dict=add_values_in_dict(content_author_dict,content_blog_authors,[content_blog_title, author_blog_content])
                
            # content_blog_authors=BlogData.objects.get(content=context_blog_data[0][0]).author
            # author_blog_content=BlogData.objects.get(author=content_blog_authors).content
            
            # print("------------------------")
            
            print(f"Final dictionary of authors and their content: {content_author_dict}")
            
            # print("---------------------------")
            
            # print(f"Check the author name: {content_blog_authors}")
            
            print("------------------------")
            # print(f"Checking the values in the dictionary {content_author_dict.items()}")
            
            for key,vals in content_author_dict.items():
                for i in range(len(content_author_dict)):
                    print(f"Key is: {key}")
                    print(f"Title: {vals[0]}")
                    print(f"Desc: {vals[1]}")
            
            
            
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
            images=individualsData.objects.all()
            # urls=images.values_list('image',flat=True)
  
            
            list_users=individualsData.objects.values_list(flat=True)
            image_path=""
            users_doi=""
            
            new_list_users=Image.objects.values_list(flat=True)
            print(f"New list of users is: {new_list_users[0]}")
            
            for new_users in new_list_users:
                user_name=Image.objects.get(id=new_users).user
                print(f"Name of New users is: {user_name}")
                users_doi=Account.objects.get(fullname=request.user).domain
                
                if str(request.user) == str(user_name):
                    # print("Yesss You are innn!!")
                    image_path=Image.objects.get(id=new_users).img
                    print(f"Domain of Interest: {users_doi}")
                    print(f"Logged in users image path is: {user_name} {image_path}")
                    break
            
            # for users in list_users:
            #     user_name=individualsData.objects.get(id=users).user
            #     users_doi=Account.objects.get(fullname=request.user).domain
            #     if str(request.user) == str(user_name):
            #         # print("Yesss You are innn!!")
            #         image_path=individualsData.objects.get(id=users).image
            #         print(f"Domain of Interest: {users_doi}")
            #         print(f"Logged in users image path is: {user_name} {image_path}")
            #         break
            #     else:
            #         # print("Oooppppss!!!")
            #         pass

            return render(request,'profile.html', context={'images':"media/"+str(image_path),
                                                           'domain_of_interest':users_doi})
    
    return render(request, 'profile.html')

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
    

def myblogs(request):
    
    users = Account.objects.filter(is_admin=False).values('fullname', 'id')
    users = list(users)
    
    for user in users:
        if request.user.is_authenticated:
            
            content_data = BlogData.objects.order_by('submitted_on').values_list('content')
            context_blog_data=[]
            
            for i in range (len(content_data)):
                context_blog_data.append(content_data[i])
            
            print(len(context_blog_data))
            title_data = BlogData.objects.values_list('title')
            context_blog_title=[]
            
            for i in range (len(title_data)):
                context_blog_title.append(title_data[i])
            
            blog_title_dict=my_dictionary()            
            
            user['show'] = True            

            for i in range(len(context_blog_data)):
                if i==4:
                    break
                else:
                    blog_title_dict.add(context_blog_title[i][0], context_blog_data[i][0])
            return render(request, 'home.html', context={'blog_data':blog_title_dict,
                                                         'admin':request.user})
        else:
            user['show'] = False
            user['content'] = "Add some Content for the blog!"
    
    if request.user.is_authenticated:
        print("Logged in!!")
        mydata = BlogData.objects.filter(user=request.user).values()
        print(mydata)
    else:
        print("Not logged in!")
    return render(request,"myblogs.html")

