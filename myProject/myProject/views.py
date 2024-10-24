from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from myApp.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core import validators
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required


# common codes start
def homePage(req):
    return render(req,'common/home.html')



@login_required
def indexPage(req):
    messages.success(req,'Log in Successful')
    return render(req,'common/index.html')

def loginPage(req):
    if req.method=='POST':
        User_name=req.POST.get('name')
        Password=req.POST.get('psw')
        if not User_name or not Password:
            messages.warning(req,'Both username and password are required')
            return render(req,"common/registerPage.html")
        
        user=authenticate(
            username=User_name,
            password=Password
            )
        if user is not None:
            login(req,user)
            messages.success(req,'Login successfully')
            return redirect('index')
        else:
            messages.warning(req,'Invalid username or password')
            
    return render(req,"common/loginpage.html")


def logoutPage(req):
    logout(req)
    messages.success(req, "You have been logged out successfully.")
    return redirect('loginPage')



def registrationPage(req):
    if req.method=='POST':
        User_name=req.POST.get('name')
        Email=req.POST.get('email')
        User_type=req.POST.get('user_type')
        Password=req.POST.get('psw')
        Confirm_password=req.POST.get('Cpsw')
        
        if not all([User_name,Email,User_type,Password]):
            messages.warning(req,'All fields are required')
            return render(req,"common/registerPage.html")
        try:
            validate_email(Email)
            
        except ValidationError:
            messages.warning(req,'Invalid Email Format')
            return render(req,"common/registerPage.html")
        
        if Password != Confirm_password:
            messages.warning(req,'Password do not match')
            return render(req,"common/registerPage.html")
        if len(Password)<8:
            messages.warning(req,'Pasword must be atleast 8 character')
            return render(req,"common/registerPage.html")
        if not any(char.isdigit() for char in Password) or not any(char.isalpha() for char in Password):
            messages.warning(req,'Password must contain both letters and number')
            return render(req,"common/registerPage.html")
        try:
            user=custom_user.objects.create_user(
                username=User_name,
                email=Email,
                user_type=User_type,
                password=Password
                )
            messages.success(req,'Account created sucessfully! Please log in')
            return redirect('loginPage')
        
        except IntegrityError:
            messages.warning(req,'Username or email already exit')
            return render(req,"common/registerPage.html")
    return render(req,"common/registerPage.html")
# common codes end 

# resume code start 



@login_required
def createresumePage(req):
    if req.user.user_type == 'viewer':
        current_user = req.user
        if req.method=="POST":
           resume=BasicInfoModel(
                user=current_user,
                contact_no=req.POST.get('contact_no'),
                designation=req.POST.get('designation'),
                career_summery=req.POST.get('career_summery'),
                age=req.POST.get('age'),
                profile_pic=req.FILES.get('profile_pic'),
           )
           resume.save()
           current_user.first_name = req.POST.get('Fname')
           current_user.last_name = req.POST.get('Lname')
           
           current_user.save()
           messages.success(req,'Resume create successfully')
           return redirect('ProfilePage')
        return render(req,'seeker/createresume.html')
    else:
        return HttpResponse("U r not authorised")
           
    

@login_required
def ProfilePage(req):
    current_user =req.user
    
    try:
        Information = get_object_or_404(BasicInfoModel, user=current_user)
        
    except Http404:
        messages.warning(req,'Both username and password are required')
        return redirect('createresumePage')
    
    languages=LanguageModel.objects.filter(user=current_user)
    skills=skillModel.objects.filter(user=current_user)
    Experience=experienceModel.objects.filter(user=current_user)
    Education=educationModel.objects.filter(user=current_user)
    
    context={
        'information':Information,
        'languages':languages,
        'skills':skills,
        'Experience':Experience,
        'Education':Education,
    }
    
    return render(req,'seeker/profile.html',context)


@login_required
def editResumePage(req):
    current_user = req.user
    information=get_object_or_404(BasicInfoModel,user=current_user)
    if req.method=="POST":
        contact_no=req.POST.get('contact_no')
        designation=req.POST.get('designation')
        Career_summery=req.POST.get('career_summery')
        Update_pic=req.FILES.get('profile_pic')
        Age=req.POST.get('age')
        Linkedin_url=req.POST.get('linkedin_url')
        Old_pic=req.POST.get('old_pic')
            
        if not designation or not Age or not contact_no:
            messages.error(req,'Plz fill the required fields')
        else:
            information.contact_no=contact_no
            information.age=Age
            information.designation=designation
            information.career_summery=Career_summery
            information.linkedin_url=Linkedin_url
            if Update_pic:
                information.profile_pic=Update_pic
            else:
                information.profile_pic=Old_pic
    
            information.save()
            messages.success(req,'Resume create successfully')
            return redirect('ProfilePage')
        
    context = {
        'information': information
    }
    return render(req,'seeker/editResume.html',context)
        




@login_required
def listbyUserPage(req):
    if req.user.user_type == 'viewer':
        current_user= req.user 
        user_skills=skillModel.objects.filter(user=current_user)
        user_Languages=LanguageModel.objects.filter(user=current_user)
        user_experiences=experienceModel.objects.filter(user=current_user)
        user_education=educationModel.objects.filter(user=current_user)
        user_interest=interestModel.objects.filter(user=current_user)
        
        
        context={
            'user_skills':user_skills,
            'user_Languages':user_Languages,
            'user_experiences':user_experiences,
            'user_education':user_education,
            'user_interest':user_interest,
        }
    return render(req,'seeker/listbyUser.html',context)

# resume code start 

# skills code start 
@login_required
def addskillPage(req):
    myMessages={
        'success_message':'Skill added successfully',
        'warning_message':'Skill added Already',
    }
    if req.user.user_type == 'viewer':
        
        All_skill=intermediate_skillModel.objects.all()
    
        current_user= req.user 
        
        if req.method == 'POST':
            skill_id=req.POST.get('skill_id')
            skill_level=req.POST.get('skill_level')
            
            my_obj= get_object_or_404(intermediate_skillModel,id=skill_id)
            
            if skillModel.objects.filter(user=current_user, skill_name=my_obj.my_skill_name).exists():
                messages.warning(req,myMessages['warning_message'])
            
            else:
                skills=skillModel(
                user=current_user,
                skill_name=my_obj.my_skill_name,
                proficiency_level=skill_level,
            )
                skills.save()
                messages.success(req,myMessages['success_message'])
                return redirect('listbyUser')
        context={
            'All_skill':All_skill,
        }
    return render(req,'seeker/addskill.html',context)



@login_required
def listEditbyUserPage(req,u_id):
    user_skills=skillModel.objects.get(id=u_id)
    all_skills=intermediate_skillModel.objects.all()
    
    current_user= req.user 
        
    if req.method == 'POST':
        skill_id=req.POST.get('skill_id')
        skill_level=req.POST.get('skill_level')
        
        my_obj= get_object_or_404(intermediate_skillModel,id=skill_id)
        
        skills=skillModel(
        user=current_user,
        id=u_id,
        skill_name=my_obj.my_skill_name,
        proficiency_level=skill_level,
        )
        skills.save()
        
        return redirect('listbyUser')
    
    context={
        'user_skills':user_skills,
        'all_skills':all_skills,
        'Proficiency_level_choices':skillModel.skill_LEVEL,
        }
    
    return render(req,'seeker/listEditbyUser.html',context)

@login_required
def dellistbyUser(req,u_id):
    user_skills=skillModel.objects.get(id=u_id).delete()
    return redirect('listbyUser')

# skills code end


# language code start
@login_required
def addLanguagePage(req):
    
    myMessages={
        'success_message':'added successfully',
        'warning_message':' added Already',
    }
    
    if req.user.user_type == 'viewer':
        
        All_Language=intermediate_LanguageModel.objects.all()
    
        current_user= req.user 
        
        if req.method == 'POST':
            Language_id=req.POST.get('Language_id')
            Language_level=req.POST.get('Language_level')
            
            my_obj= get_object_or_404(intermediate_LanguageModel,id=Language_id)
            
            if LanguageModel.objects.filter(user=current_user, Language_name=my_obj.my_Language_name).exists():
                messages.warning(req,myMessages['warning_message'])
            
            else:
                Languages=LanguageModel(
                user=current_user,
                Language_name=my_obj.my_Language_name,
                proficiency_level=Language_level,
            )
                Languages.save()
                messages.success(req,myMessages['success_message'])
                return redirect('listbyUser')
        context={
            'All_Language':All_Language,
        }
    return render(req,'seeker/addlanguage.html',context)


@login_required
def languageEditbyUserPage(req,u_id):
    user_language=LanguageModel.objects.get(id=u_id)
    all_languages=intermediate_LanguageModel.objects.all()
    
    current_user= req.user 
        
    if req.method == 'POST':
        Language_id=req.POST.get('language_id')
        Language_level=req.POST.get('language_level')
        
        my_obj= get_object_or_404(intermediate_LanguageModel,id=Language_id)
        
        Languages=LanguageModel(
        user=current_user,
        id=u_id,
        Language_name=my_obj.my_Language_name,
        proficiency_level=Language_level,
        )
        Languages.save()
        
        return redirect('listbyUser')
    
    context={
        'user_language':user_language,
        'all_languages':all_languages,
        'proficiency_level':LanguageModel.Language_LEVEL,
        }
    
    return render(req,'seeker/languageEditbyUser.html',context)


@login_required
def delLanguagebyUser(req,u_id):
    user_Language=LanguageModel.objects.get(id=u_id).delete()
    return redirect('listbyUser')

# language code end

# experience code start 

@login_required
def addexperiencePage(req):
    
    myMessages={
        'success_message':' Added successfully',
        'warning_message':' Added Already',
    }
    
    if req.user.user_type == 'viewer':
        
        All_experience=intermediate_experienceModel.objects.all()
    
        current_user= req.user 
        
        if req.method == 'POST':
            Experience_id=req.POST.get('experience_id')
            Experience_level=req.POST.get('experience_level')
            
            my_obj= get_object_or_404(intermediate_experienceModel,id=Experience_id)
            
            if experienceModel.objects.filter(user=current_user, experience_name=my_obj.my_experience_name).exists():
                messages.warning(req,myMessages['warning_message'])
            
            else:
                experiences=experienceModel(
                user=current_user,
                experience_name=my_obj.my_experience_name,
                proficiency_level=Experience_level,
            )
                experiences.save()
                messages.success(req,myMessages['success_message'])
                return redirect('listbyUser')
        context={
            'All_experience':All_experience,
        }
    return render(req,'seeker/addexperience.html',context)


@login_required
def delexperiencesbyUser(req,u_id):
    user_experiences=experienceModel.objects.get(id=u_id).delete()
    return redirect('listbyUser')


@login_required
def experienceEditbyUserPage(req,u_id):
    user_experience=experienceModel.objects.get(id=u_id)
    all_experience=intermediate_experienceModel.objects.all()
    
    current_user= req.user 
        
    if req.method == 'POST':
        Experience_id=req.POST.get('experience_id')
        Experiences_level=req.POST.get('experiences_level')
        
        my_obj= get_object_or_404(intermediate_experienceModel,id=Experience_id)
        
        experiences=experienceModel(
        user=current_user,
        id=u_id,
        experience_name=my_obj.my_experience_name,
        proficiency_level=Experiences_level,
        )
        experiences.save()
        
        return redirect('listbyUser')
    
    context={
        'user_experience':user_experience,
        'all_experience':all_experience,
        'Proficiency_level_choices':experienceModel.experience_LEVEL,
        }
    
    return render(req,'seeker/experienceEditbyUser.html',context)
# experience code end 

# education codes start 

@login_required
def addeducationPage(req):
    
    myMessages={
        'success_message':' Added successfully',
        'warning_message':' Added Already',
    }
    
    if req.user.user_type == 'viewer':
        
        All_education=intermediate_educationModel.objects.all()
    
        current_user= req.user 
        
        if req.method == 'POST':
            education_id=req.POST.get('education_id')
            education_level=req.POST.get('education_level')
            
            my_obj= get_object_or_404(intermediate_educationModel,id=education_id)
            
            if educationModel.objects.filter(user=current_user, education_name=my_obj.my_education_name).exists():
                messages.warning(req,myMessages['warning_message'])
            
            else:
                education=educationModel(
                user=current_user,
                education_name=my_obj.my_education_name,
                proficiency_level=education_level,
            )
                education.save()
                messages.success(req,myMessages['success_message'])
                return redirect('listbyUser')
        context={
            'All_education':All_education,
        }
    return render(req,'seeker/addeducation.html',context)

@login_required
def deleducationbyUser(req,u_id):
    user_experiences=educationModel.objects.get(id=u_id).delete()
    return redirect('listbyUser')



@login_required
def educationEditbyUserPage(req,u_id):
    user_education=educationModel.objects.get(id=u_id)
    all_education=intermediate_educationModel.objects.all()
    
    current_user= req.user 
        
    if req.method == 'POST':
        Education_id=req.POST.get('education_id')
        Education_level=req.POST.get('education_level')
        
        my_obj= get_object_or_404(intermediate_educationModel,id=Education_id)
        
        Education=educationModel(
        user=current_user,
        id=u_id,
        education_name=my_obj.my_education_name,
        proficiency_level=Education_level,
        )
        Education.save()
        
        return redirect('listbyUser')
    
    context={
        'user_education':user_education,
        'all_education':all_education,
        'Proficiency_level_choices':educationModel.education_LEVEL,
        }
    
    return render(req,'seeker/educationEditbyUser.html',context)


# education codes end 

# interest codes start 

@login_required
def addinterestPage(req):
    
    myMessages={
        'success_message':' Added successfully',
        'warning_message':' Added Already',
    }
    
    if req.user.user_type == 'viewer':
        
        All_interest=intermediate_interestModel.objects.all()
    
        current_user= req.user 
        
        if req.method == 'POST':
            Interest_id=req.POST.get('interest_id')
            Interest_level=req.POST.get('interest_level')
            
            my_obj= get_object_or_404(intermediate_interestModel,id=Interest_id)
            
            if interestModel.objects.filter(user=current_user, interest_name=my_obj.my_interest_name).exists():
                messages.warning(req,myMessages['warning_message'])
            
            else:
                Interest=interestModel(
                user=current_user,
                interest_name=my_obj.my_interest_name,
                proficiency_level=Interest_level,
            )
                Interest.save()
                messages.success(req,myMessages['success_message'])
                return redirect('listbyUser')
        context={
            'All_interest':All_interest,
        }
    return render(req,'seeker/addinterest.html',context)

@login_required
def delinterestbyUser(req,u_id):
    user_interest=interestModel.objects.get(id=u_id).delete()
    return redirect('listbyUser')


@login_required
def interestEditbyUserPage(req,u_id):
    user_interest=interestModel.objects.get(id=u_id)
    all_interest=intermediate_interestModel.objects.all()
    
    current_user= req.user 
        
    if req.method == 'POST':
        Interest_id=req.POST.get('interest_id')
        Interest_level=req.POST.get('interest_level')
        
        my_obj= get_object_or_404(intermediate_interestModel,id=Interest_id)
        
        interests=interestModel(
        user=current_user,
        id=u_id,
        interest_name=my_obj.my_interest_name,
        proficiency_level=Interest_level,
        )
        interests.save()
        
        return redirect('listbyUser')
    
    context={
        'user_interest':user_interest,
        'all_interest':all_interest,
        'Proficiency_level_choices':interestModel.interest_LEVEL,
        }
    
    return render(req,'seeker/interestEditbyUser.html',context)


# interest codes end 

