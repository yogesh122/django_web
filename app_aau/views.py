from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.http import Http404
from .models import *
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView,FormView)
from django.contrib.auth.decorators import login_required
# from .hf import *
from app_aau import helper_functions as hf
from django.urls import reverse_lazy,reverse
# use mixins for Class based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout,get_user_model
from django.contrib.auth.models import User as main_user
# Create your views here.
# Form import
from . import form

import pandas as pd
import numpy as np
import os
import time

from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

from django.http import HttpResponse

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

import string
from random import *

'''
When user comes to website.
Depending on the user type such as student, hod, instructor, registrar,
dean welcome page will shown.

If not login redirected to login page.
'''
class IndexPage(LoginRequiredMixin,TemplateView):
    template_name = ""

    def get_context_data(self, **kwargs):
        context  =  super(IndexPage, self).get_context_data(**kwargs)

        # Check are kept based on the type login.
        if hf.student_check(self.request.user):
            IndexPage.template_name  =  'student/student_index.html'
        elif hf.hod_check(self.request.user):
            IndexPage.template_name  =  'instructor/hod_index.html'
        elif hf.instructor_check(self.request.user):
            # Sending the file list to instructor and
            # display file name and reseaon of file which are rejected.
            user_obj  =  get_object_or_404(get_user_model(), email  =  self.request.user)
            context['instructor_file_list']  =  TempFile.objects.filter(
            instructor__user  =  user_obj)
            IndexPage.template_name  =  'instructor/instructor_index.html'
        elif hf.registrar_check(self.request.user):
            IndexPage.template_name  =  'registrar/index.html'
        elif hf.dean_check(self.request.user):
            IndexPage.template_name  =  'dean/index.html'
        else:
            IndexPage.template_name = 'error.html'
            context['error_message']  =  "You have not login. Please login to proceed further"
            logout(self.request)

        return context


# Model form for password change
pass_form  =  form.Password_change_Form()
password_change_dict = {'pass_form':pass_form,'pass_message':""}

'''
Check whether the login is done or not and also check whether its student, dean, instructor or dean.
Than, it will take the previous password and match whether previous password match with existing or not.
Than, if the new password and confirm password are same than password of the user get changed.
'''
@login_required
def pass_change(request):

    if request.method == 'POST':
        if (hf.student_check(request.user) or
            hf.instructor_check(request.user) or
            hf.registrar_check(request.user) or
            hf.dean_check(request.user)):

            pass_form  =  form.Password_change_Form(request.POST)
            previous_password  =  request.POST.get('previousPassword')

            # confirm  =  request.POST.get('confirm_password')
            user_password  =  request.POST.get('password')
            user_confirmed_password  =  request.POST.get('confirm_password')

            if(pass_form.is_valid()):
                if(hf.check_previous_password(previous_password,request.user)):
                    if(hf.change_user_password(request.user,user_password,user_confirmed_password)):
                        password_change_dict['pass_message'] = "Password Change"
                    else:
                        password_change_dict['pass_message'] = "Password and confirmed password does not match"
                else:
                    password_change_dict['pass_message'] = "Previous Password does not match"
            else:
                password_change_dict['pass_message'] = "Form is not valid"

            return render(request,'password_change.html',password_change_dict)
        else:
            error_message = {'error_message':"Password Form can't be open"}

            return render(request,'error_message.html',error_message)
    else:
        return render(request,'password_change.html',password_change_dict)


'''
When Instructor or hod upload the file contianing marks.
It will first check whether they are instructor or not.
If yes, than the file is checked --> uses student_roll_check function.
If the data in excel is properly entered the gets upload and if not than proper message is displayed.

'''
class InstructorFileUpload(LoginRequiredMixin,CreateView):
    form_class  =  form.File_Upload
    model  =  TempFile

    template_name = "instructor/instructor_upload.html"

    def form_valid(self,form):
        if hf.instructor_check(self.request.user):
            print("In form validation")
            file_path  =  self.get_form_kwargs().get('files')['file_path']
            file_name  =  file_path.name

            print(super().form_valid(form),"   Here is primary key: ", self.object.pk,"  ",self.request.user)

            std_roll  =  hf.student_roll_check(file_name,self.request.user)
            print(std_roll)

            if (std_roll['reply_code'] == 1) and hf.add_file_to_instructor(self.request.user,self.object.pk):
                self.object  =  form.save(commit  =  False)
                self.object.file_name  =  std_roll['reply_message']
                self.object.file_path  =  os.path.join('instructor_file',std_roll['reply_message'])
                self.object.save()
                return redirect('instructor_upload_message',upload_message = "Your file is uploaded")
            elif(std_roll['reply_code'] == 2):
                InstructorFileUpload.clear_empty_file()
                return redirect('instructor_upload_message',upload_message  =  std_roll['reply_message'])
            elif(std_roll['reply_code'] == 3):
                InstructorFileUpload.clear_empty_file()
                return redirect('instructor_upload_message',upload_message  =  std_roll['reply_message'])
            elif(std_roll['reply_code'] == 4):
                InstructorFileUpload.clear_empty_file()
                return redirect('instructor_upload_message',upload_message  =  std_roll['reply_message'])
            elif(std_roll['reply_code'] == 5):
                InstructorFileUpload.clear_empty_file()
                return redirect('instructor_upload_message',upload_message  =  std_roll['reply_message'])
            elif(std_roll['reply_code'] == 6):
                InstructorFileUpload.clear_empty_file()
                return redirect('instructor_upload_message',upload_message  =  std_roll['reply_message'])

            else:
                InstructorFileUpload.clear_empty_file()
                return redirect('instructor_upload_message',upload_message = "Error uploading file and adding to database.")

            try:
                TempFile.objects.filter(file_name = '').delete()
            except Exception as e:
                print("Here is the error message: ",e)
                pass

        else:
            logout(self.request)
            return redirect('login')

    def clear_empty_file():
        try:
            TempFile.objects.filter(file_name = '').delete()
        except Exception as e:
            print(e)
            pass


    def get_context_data(self, **kwargs):
        print("In context_data")
        context  =  super(InstructorFileUpload, self).get_context_data(**kwargs)
        context['file_message']  =  ""#{}message
        return context

"""
View uploaded file- Instructor, HOD, Dean, Registrar
Gets the department of the user. One user would be having only one instructor.
For Hod file of user with specific department name for hod.
For instructor based on only user_obj.
For dean and Registrar all file.
"""
class View_Uploaded_File(LoginRequiredMixin,TemplateView):

    template_name = ""
    model  =  TempFile
    reject_reason_form  =  form.Reject_reason_Form()
    def get_context_data(self, **kwargs):
        context  =  super(View_Uploaded_File, self).get_context_data(**kwargs)
        # print(self.request.user)
        d_name  =  Department.objects.filter(instructor__user  =  self.request.user).values('Department_name')

        try:
            TempFile.objects.filter(file_name = '').delete()
        except Exception as e:
            # print(e)
            pass

        if hf.instructor_check(self.request.user) and hf.hod_check(self.request.user):
            context['upload_file_list']  =  TempFile.objects.filter(instructor__instructor_department =
                            (Department.objects.get(Department_name  =  str(
                                d_name[0]['Department_name'])
                                ))).order_by('-created')

            context['department_name']  = str(d_name[0]['Department_name'])

            context['reject_reason_form'] = View_Uploaded_File.reject_reason_form

            View_Uploaded_File.template_name = 'instructor/hod_view_file.html'
            # print(str(self.request.user)+" (HOD) viewed uploaded file")

        elif hf.instructor_check(self.request.user):
            # print("In instructor only")
            user_obj  =  get_object_or_404(get_user_model(), email  =  self.request.user)
            context['upload_file_list'] = TempFile.objects.filter(instructor__user =  user_obj).order_by('-created')
            # print(TempFile.objects.filter(instructor__user =  user_obj))
            context['department_name']  = str(d_name[0]['Department_name'])
            View_Uploaded_File.template_name = 'instructor/instructor_view_uploaded_file.html'
            # print(str(self.request.user) +" (Instructor) viewed uploaded file")

        elif hf.registrar_check(self.request.user):
            print("Only registrar")
            context['upload_file_list'] = TempFile.objects.all().order_by('-created')
            # .order_by('file_time_stamp'.desc()).
            # print(TempFile.objects.all())

            context['reject_reason_form'] = View_Uploaded_File.reject_reason_form

            View_Uploaded_File.template_name = 'registrar/registrar_view_file.html'
            # print(str(self.request.user)+" (Registrar) viewed uploaded file")

        elif hf.dean_check(self.request.user):
            context['upload_file_list'] = TempFile.objects.all().order_by('-created')

            context['reject_reason_form'] = View_Uploaded_File.reject_reason_form

            View_Uploaded_File.template_name = 'dean/dean_view_file.html'
            # print(str(self.request.user)+" (Dean) viewed uploaded file")

        else:
            View_Uploaded_File.template_name = 'error.html'
            context['error_message']  =  "Your are not Authorized to login in. To access this page please login."
            logout(self.request)

        return context

'''
Only hod can add courses.
Multiple course are added using add_multiple_course_function
'''
@login_required
def add_multiple_course(request):
    if request.method == 'POST':
        forms  =  form.RegistrarUploadFile(request.POST, request.FILES)
        if forms.is_valid():
            # request.POST.get()
            get_file  =  request.FILES['file']
            get_file_name  =  get_file.name

        if not(hf.hod_check(hod_obj)):
            return render(request,'error.html',{'error_message':"Only Hod can access this functionality."})

        if (get_file_name.endswith(".xlsx") or get_file_name.endswith(".xls")):
            course_upload  =  pd.read_excel(get_file,sheet_name  =  0,)
            return_message  =  hf.add_multiple_course_function(course_upload)
            return render(request,'instructor/course_message.html',{'message':return_message})
        else:
            return render(request,'error.html',{'error_message':"Please upload Excel sheet"})
    else:
        return render(request,'instructor/add_course.html',{'registrar_form': registrar_upload_form})

'''
Templates are only for instructor/hod and registrar
'''
@login_required
def template_page(request):
    if hf.instructor_check(request.user):
        return render(request,'instructor/template.html')
    elif hf.registrar_check(request.user):
        return render(request,'registrar/template.html')
    else:
        logout(request)
        error_message = {'error_message':"You dont have access to this page."}
        return render(request,'error_message.html',error_message)

'''
Used to print the message when file is uploaded.
'''
@login_required
def FileUploadMessage(request,upload_message):
    file_messages = {'file_message':upload_message}
    return render(request,'instructor/file_upload_message.html',file_messages)

'''
When hod approve the file.
Make the file_uplaoded_hod = True
'''
@login_required
def approved_marks_by_hod(request):
    if request.method == 'POST':
        file_name = request.POST.get('get_file_name')
        try:
            tt = TempFile.objects.get(file_name = file_name, file_rejected = False)
            tt.file_uploaded_hod  =  True
            tt.save()
            return redirect('view_file_upload')
        except Exception as e:
            print(e)
            tt  =  TempFile.objects.get(file_name = file_name,file_uploaded_hod = False).delete()
            root_file  =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            excel_dir  =  os.remove(os.path.join(root_file,'media','instructor_file',file_name))
            return render(request,'error.html',{'error_message':"File is alredy exists in approved folder"})
    else:
        logout(request)
        return render(request,'error.html',{'error_message':"You are trying to access unoffical things"})

'''
When dean approve the file.
Make the file_uplaoded_dean = True
'''
@login_required
def approve_marks_dean(request):
    if request.method == 'POST':
        file_name  =  request.POST.get('get_file_name')
        try:
            print("In HOD approve")
            tt  =  TempFile.objects.get(file_name  =  file_name,file_rejected  =  False)
            tt.file_uploaded_dean  =  True
            tt.save()
            print("In HOD approve end")
            return redirect('view_file_upload')
        except Exception as e:
            print("Here is error message: ",e)
            return render(request,'error.html',{'error_message':"Marks are not uploaded to database"})

'''
When registrar approve the file.
Make the file_uplaoded_registrar = True
'''
@login_required
def approve_marks_registrar(request):
    if request.method == 'POST':
        file_name  =  request.POST.get('get_file_name')
        try:
            tt  =  TempFile.objects.get(file_name  =  file_name,file_rejected  =  False)
            tt.file_uploaded_registrar  =  True
            tt.save()
            return redirect('view_file_upload')
        except Exception as e:
            print(e)
            return render(request,'error.html',{'error_message':"Marks are not uploaded to database"})

'''
When hod/dean/registrar reject the file.
Make the file_rejected = True
move file to media/rejected file by changing file.
'''
@login_required
def rejected_marks_file(request):
    if request.method == 'POST':
        file_name  =  request.POST.get('get_file_name')
        try:
            tt  =  TempFile.objects.get(file_name  =  file_name,file_rejected  =  False)
            root_file  =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_dir  =  os.path.join(root_file,'media',str(tt.file_path))
            rejected_file_name  =  hf.random_name()+"_"+str(file_name)
            rejected_dir  =  os.path.join(root_file,'media','rejected',rejected_file_name)
            os.rename(file_dir,rejected_dir)
            if(hf.registrar_check(request.user)):
                tt.file_status = "File Rejected by Registrar"
            elif(hf.hod_check(request.user)):
                tt.file_status = "File Rejected by HOD"
            elif(hf.dean_check(request.user)):
                tt.file_status = "File Rejected by Dean"
            tt.file_rejected  =  True
            tt.file_path  =  os.path.join('rejected',file_name)
            tt.save()
            return redirect('view_file_upload')
        except Exception as e:
            print(e)
            return render(request,'error.html',{'error_message':"File is alredy exists in approved folder"})
    else:
        logout(request)
        return render(request,'error.html',{'error_message':"You are trying to access unoffical things"})

'''
When hod/dean/registrar added the reason for rejecting the file.
'''
@login_required
def reject_marks_reason(request):
    if request.method == 'POST':
        file_name  =  request.POST.get('get_file_name')
        file_reject_message  =  request.POST.get('reject_message')
        print(file_reject_message, "   ",type(file_reject_message))
        try:
            tt  =  TempFile.objects.get(pk  =  file_name)
            if(hf.registrar_check(request.user)):
                tt.file_status = "Registrar: "+file_reject_message
            elif(hf.hod_check(request.user)):
                tt.file_status = ("HOD: "+str(file_reject_message))
            elif(hf.dean_check(request.user)):
                tt.file_status = "Dean: "+file_reject_message
            tt.file_rejected_reason  =  True
            tt.save()
            return redirect('view_file_upload')
        except Exception as e:
            print(e)
            return render(request,'error.html',{'error_message':"File is alredy exists in approvedddd folder"})
    else:
        logout(request)
        return render(request,'error.html',{'error_message':"You are trying to access unoffical things"})

'''
Get result of student based on user.
'''
class StudentResult(LoginRequiredMixin,TemplateView):
    template_name = ""

    def get_context_data(self, **kwargs):

        context  =  super(StudentResult, self).get_context_data(**kwargs)
        if hf.student_check(self.request.user):
            context['result_dict']  =  hf.get_result(self.request.user)
            StudentResult.template_name = "student/student_result.html"
        else:
            StudentResult.template_name = 'error.html'
            context['error_message']  =  "Your are not a student. Please login with student credentials"
            logout(self.request)

        return context


'''
Relase marks of file by registrar
make marks_release true
'''
@login_required
def release_marks(request):
    if request.method == 'POST':
        file_name  =  request.POST.get('get_file_name')
        try:
            hf.marks_upload(file_name)
            tt  =  TempFile.objects.get(file_name  =  file_name,file_rejected  =  False)
            tt.marks_release  =  True
            tt.save()

        except Exception as e:
            print(e)
        return redirect('view_file_upload')
    else:
        logout(request)
        return render(request,'error.html',{'error_message':"You are trying to access unoffical things"})

'''
Download file.
'''
@login_required
def file_download(request,fileName):
    # print(fileName)
    tt  =  TempFile.objects.get(file_name  =  fileName, file_rejected  =  False)
    # print(tt.file_path)
    filePath  =  os.path.join('media',str(tt.file_path))
    print(filePath)
    if os.path.exists(filePath):
        with open(filePath, 'rb') as fh:
            response  =  HttpResponse(fh.read(), content_type = "application/vnd.ms-excel")
            response['Content-Disposition']  =  'inline; filename = ' + os.path.basename(filePath)
            return response
            # return render(request,'test.html')
    raise Http404

'''
Download result pdf of student.
'''
@login_required
def download_result(request):

    if(hf.download_result_function(request.user) == True):
        filePath  =  os.path.join('media','test',str(request.user.first_name)+'_result.pdf')
        print(filePath)
        if os.path.exists(filePath):

            fsock  =  open(filePath, 'r')
            response  =  HttpResponse(fsock, content_type = "application/pdf")
            # response['Content-Disposition']  =  'inline;filename = '+str(request.user.first_name)+'_result.pdf'#+ os.path.basename(filePath)
            response['Content-Disposition']  =  'inline;filename = '+ os.path.basename(filePath)
                # response['Content-Disposition']  =  'inline; filename = ' + os.path.basename(filePath)
            root_file  =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            os.remove(os.path.join(root_file,filePath))

            return response
        else:
            return render(request,'error.html',{'error_message':"Error downloading result (PDF)"})        # return render(request,'test.html')

        # return render(request,'error.html',{'error_message':"WOWOWOOW,Created file"})
    else:
        return render(request,'error.html',{'error_message':"Can't download file."})

'''
Registrar can add multiple student to database.
Add multiple_student_function is used to upload multiple students to database
'''
registrar_upload_form  =  form.RegistrarUploadFile()
@login_required
def add_multiple_student(request):
    if request.method == 'POST':
        forms  =  form.RegistrarUploadFile(request.POST, request.FILES)
        if forms.is_valid():
            # request.POST.get()
            get_file  =  request.FILES['file']
            get_file_name  =  get_file.name
        # print(get_file)

            if (get_file_name.endswith(".xlsx") or get_file_name.endswith(".xls")):
                student_upload  =  pd.read_excel(get_file,sheet_name  =  0,)
                return_message  =  hf.add_multiple_student_function(student_upload)
                return render(request,'registrar/student_message.html',{'message':return_message})
            else:
                return render(request,'error.html',{'error_message':"Please upload Excel sheet"})
        else:
            return render(request,'error.html',{'error_message':"Error uploading student. Try again!"})


    else:
        return render(request,'registrar/add_students.html',{'registrar_form': registrar_upload_form})

'''
Download template.
'''
@login_required
def template_download(request,fileName):

    if hf.registrar_check(request.user) :
        if fileName=='add_student_template':
            filePath = os.path.join('media','template',fileName+'.xlsx')
        else:
            error_message={'error_message':"File not found."}
            return render(request,'error.html',error_message)

    elif hf.hod_check(request.user):
        if fileName=='add_course_template' or fileName=='marks_template':
            filePath = os.path.join('media','template',fileName+'.xlsx')
        else:
            error_message={'error_message':"File not found."}
            return render(request,'error.html',error_message)

    elif hf.instructor_check(request.user):
        if fileName=='marks_template':
            filePath = os.path.join('media','template',fileName+'.xlsx')
        elif fileName=='add_course_template':
            error_message={'error_message':"You cannot access this file."}
            return render(request,'error.html',error_message)
        else:
            error_message={'error_message':"File not found."}
            return render(request,'error.html',error_message)

    else:
        error_message={'error_message':"You do not have access to download this files."}
        return render(request,'error.html',error_message)

    # print(filePath)
    if os.path.exists(filePath):
        with open(filePath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filePath)
            return response
    raise Http404
