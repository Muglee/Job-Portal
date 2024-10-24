from django.shortcuts import render,redirect,get_object_or_404
from myApp.models import *
from django.contrib import messages
from django.templatetags.static import static
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q

def addjobPage(req):
    current_user =req.user
    if current_user.user_type =="admin":
        if req.method == 'POST':
            job=JobModel()
            job.user=current_user
            job.job_title=req.POST.get('jobTitle')
            job.Description=req.POST.get('jobDescription')
            job.Requirements=req.POST.get('jobRequirements')
            job.Company_name=req.POST.get('companyName')
            job.company_logo=req.FILES.get('c_logo')
            job.Location=req.POST.get('location')
            job.qualification=req.POST.get('qualifications')
            job.application_deadline=req.POST.get('deadline')
            job.save()
            messages.success(req,'Job created Successfully')
            return redirect('jobfeed')
        return render(req,'myAdmin/addjob.html')
    else:
        messages.warning(req,"You are not recruited")
        
        
def createdJobPage(req):
    current_user= req.user
    create_job=JobModel.objects.filter(user=current_user)
    
    context={
        "Job":create_job,
    }
    return render(req,'myAdmin/createdjob.html',context)

def applicantListPage(req,job_id):
    job=get_object_or_404(JobModel,id=job_id)
    applications = jobApplyModel.objects.filter(job=job)
    context={
        'job':job,
        'applications':applications,
        }
    return render(req,'myAdmin/applicantList.html',context)
    
    
    
def callForInterview(request, job_id, application_id):
    application = get_object_or_404(jobApplyModel, id=application_id)

    application.status = 'interview_scheduled'  
    application.save()

    messages.success(request, 'The applicant has been called for an interview.')
    return redirect('applicantList', job_id=job_id)


def rejectApplication(request, job_id, application_id):
    application = get_object_or_404(jobApplyModel, id=application_id)

    # Reject the application
    application.status = 'rejected'  
    application.save()

    messages.success(request, 'The application has been rejected.')

    application_messages = MessageModel.objects.filter(application=application)

    context = {
        'job_id': job_id,
        'application': application,
        'messages': application_messages
    }

    return redirect('applicantList', job_id=job_id)


def message_list(request, job_id):
    job = get_object_or_404(JobModel, id=job_id)
    messages = MessageModel.objects.filter(application__job=job)

    context = {
        'job': job,
        'messages': messages
    }
    
    return render(request, 'myAdmin/message_list.html', context)


def sendMessage(req,job_id,application_id):
    current_user = req.user
    job = get_object_or_404(JobModel,id=job_id)
    application = get_object_or_404(jobApplyModel,id=application_id)
    context= {
        'job':job,
        'application':application, 
    }
    if req.method == 'POST':
        content = req.POST.get('messageText')
        recipient = application.user
        # check for duplicate messages 
        if MessageModel.objects.filter(
            application=application,
            sender=current_user,
            content=content,
            timestamp__gte=timezone.now() - timezone.timedelta(minutes = 1) # Check if sent within the last minute
        ).exists():
            messages.error(req,'you have already sent this message')
            return redirect('message_list',job_id = job_id)
        # if no duplicate ,save the message 
        message = MessageModel(
            application=application,
            sender=current_user,
            content=content,
            timestamp__gte=timezone.now()
        )
        message.save()
        messages.success(req,'Message sent successfully!')
        return redirect('message_list',job_id = job_id)
    else:
        return render(req,'myAdmin/sendMessage.html')