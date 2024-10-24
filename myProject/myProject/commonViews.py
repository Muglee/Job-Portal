from django.shortcuts import render,redirect,get_object_or_404
from myApp.models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q




# search job 
def searchJob(req):
    query = req.GET.get('query')
    if query:
        jobs = JobModel.objects.filter(Q(job_title_icontains= query)
                                       |Q(description_icontains= query)
                                       |Q(employment_icontains= query)
                                       |Q(company_icontains= query)
                                       )
        
    else:
        jobs = JobModel.objects.none()
    
    context={
        'jobs':jobs,
        'query':query,
        
    }
    return render(req,'common/search.html')


# change password 

def changePswPage(req):
    current_user=req.user
    if req.method=='POST':
        Current_Password=req.POST.get('current-password')
        New_Password=req.POST.get('new-password')
        Confirm_Password=req.POST.get('confirm-password')
        if check_password(Current_Password,req.user.password):
            if New_Password == Confirm_Password:
                current_user.set_password(New_Password)
                current_user.save()
                messages.success(req,'Password Changed Successfully')
            
    return render(req,'common/changepassword.html')
    
    
# job feed start 

def jobfeedPage(req):
    job=JobModel.objects.all()
    context={
        'job':job
    }
    return render(req,'common/jobfeed.html',context)


def applyNowPage(req,job_title,j_id):
    current_user=req.user
    if current_user.user_type == 'viewer':
        specific_job=JobModel.objects.get(id=j_id)
        already_exist = jobApplyModel.objects.filter(user=current_user,job=specific_job).exists()
        context={
            'specific_job':specific_job,
            'already_exist':already_exist,
        }
        if req.method == 'POST':
            Full_name = req.POST.get('full_name')
            Resume = req.POST.get('resume')
            Cover_letter = req.POST.get('cover_letter')
            Work_experience = req.POST.get('work_experience')
            Skills = req.POST.get('skills')
            Linkedin_url = req.POST.get('linkedin_url')
            Expected_salary = req.POST.get('expected_salary')
            Apply = jobApplyModel(
                user=current_user,
                job=specific_job,
                Resume=Resume,
                Full_name=Full_name,
                cover_letter=Cover_letter,
                work_experience=Work_experience,
                skills=Skills,
                Linkedin_url=Linkedin_url,
                Expected_salary=Expected_salary,
            )
            Apply.save()
            return redirect('jobfeed')
        return render(req,'seeker/applyNow.html',context)
    else:
        messages.warning(req,"You are not a jobseeker")
        
        
        
def proPage(req):
    data=BasicInfoModel.objects.all()
    
    context={
        'data':data,
    }
    return render(req,'myAdmin/proPage.html',context)


def viewJobPage(req,view_id):
    view_job_data=JobModel.objects.get(id=view_id)
    context={
        'job':view_job_data,
    }
    return render(req,'seeker/viewJob.html',context)