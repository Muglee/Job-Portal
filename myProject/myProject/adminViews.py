from django.shortcuts import render,redirect,get_object_or_404
from myApp.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def add_job_Page(req):
    if req.method == 'POST':
        job_title = req.POST.get('job_title')
        Company_name = req.POST.get('company_name')
    return render(req,'addjob.html')