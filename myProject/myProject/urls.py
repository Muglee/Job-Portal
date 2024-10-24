"""
URL configuration for myProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myProject.views import *
from myProject.commonViews import *
from myProject.recruiterviews import *


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', homePage,name='home'),
    path('index/', indexPage,name='index'),
    path('registrationPage/', registrationPage,name='registrationPage'),
    path('', loginPage,name='loginPage'),
    path('logoutPage/', logoutPage,name='logoutPage'),
    path('changePsw/', changePswPage,name='changePsw'),
    
    path('jobfeed/', jobfeedPage, name='jobfeed'),
    path('applyNow/<str:job_title>/<str:j_id>/', applyNowPage, name='applyNow'),
    
    
    path('proPage/', proPage, name='proPage'),
    
    # recruiter
    
    path('addjob/', addjobPage, name='addjob'),
    path('createdJob/', createdJobPage, name='createdJob'),
    path('applicants/<int:job_id>', applicantListPage, name='applicantList'),
    path('job/<int:job_id>/messages/', message_list, name='message_list'),
    path('job/<int:job_id>/application/<int:application_id>/sendMessages/', sendMessage, name='sendMessage'),
    path('job/<int:job_id>/applicants/<int:application_id>/interview/',callForInterview, name='call_for_interview'),
    path('job/<int:job_id>/applicants/<int:application_id>/reject/',rejectApplication, name='reject_application'),
    
    
    # seeker 
    path('viewJob/<str:view_id>/', viewJobPage, name='viewJob'),
    
    
    # resume urls 
    path('createresumePage/', createresumePage,name='createresumePage'),
    path('ProfilePage/', ProfilePage,name='ProfilePage'),
    path('editResume/', editResumePage,name='editResume'),
    
    # add functions urls 
    
    path('addskill/', addskillPage,name='addskill'),
    path('addLanguage/', addLanguagePage,name='addLanguage'),
    path('addexperience/', addexperiencePage,name='addexperience'),
    path('addeducationPage/', addeducationPage,name='addeducationPage'),
    path('addinterest/', addinterestPage,name='addinterest'),
    path('listbyUser/', listbyUserPage,name='listbyUser'),
    path('listEditbyUser/<str:u_id>', listEditbyUserPage,name='listEditbyUser'),
    path('languageEditbyUser/<str:u_id>', languageEditbyUserPage,name='languageEditbyUser'),
    path('experienceEditbyUser/<str:u_id>', experienceEditbyUserPage,name='experienceEditbyUser'),
    path('educationEditbyUser/<str:u_id>', educationEditbyUserPage,name='educationEditbyUser'),
    path('interestEditbyUser/<str:u_id>', interestEditbyUserPage,name='interestEditbyUser'),
    path('dellistbyUser/<str:u_id>', dellistbyUser,name='dellistbyUser'),
    path('delexperiencesbyUser/<str:u_id>', delexperiencesbyUser,name='delexperiencesbyUser'),
    path('delLanguagebyUser/<str:u_id>', delLanguagebyUser,name='delLanguagebyUser'),
    path('deleducationbyUser/<str:u_id>', deleducationbyUser,name='deleducationbyUser'),
    path('delinterestbyUser/<str:u_id>', delinterestbyUser,name='delinterestbyUser'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
