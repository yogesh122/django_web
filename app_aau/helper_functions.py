from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.http import Http404
from .models import *
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView,FormView)
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy,reverse
# use mixins for Class based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout,get_user_model
from django.contrib.auth.models import User as main_user
# Create your views here.
# Form import
from . import form

import pandas as pd
import os
import numpy as np
import time

from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

##############################
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Image,Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
############################
from django.http import HttpResponse

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

import string
from random import *

def hod_check(user_name):
    print("Checking hod authentication ")
    check_hod_authentication = Instructor.objects.filter(user = user_name, is_instructor_hod = True).exists()
    print("Done Checking hod authentication")
    return check_hod_authentication

def student_check(user_name):
    print("Checking student authentication ")
    check_student_authentication = Student.objects.filter(user = user_name).exists()
    print("Done Checking student authentication")
    return check_student_authentication

def instructor_check(user_name):
    print("Checking instructor authentication ")
    check_instructor_authentication = Instructor.objects.filter(user = user_name).exists()
    print("Done Checking instructor authentication")
    return check_instructor_authentication

def registrar_check(user_name):
    print("Checking Registrar authentication")
    check_registrar_authentication = Registrar.objects.filter(user = user_name).exists()
    print("Done Checking Registrar authentication")
    return check_registrar_authentication

def dean_check(user_name):
    print("Checking Dean authentication")
    check_dean_authentication = Dean.objects.filter(user = user_name).exists()
    print("Done Checking Dean authentication")
    return check_dean_authentication

def check_previous_password(previous_password,user_obj):
    user_check = authenticate(email = user_obj.email, password = previous_password)
    if (user_check!=None):
        return True
    else:
        return False

def change_user_password(uss,ps,confirm_pass):
    if(ps==confirm_pass):
        us = get_user_model().objects.get(email = uss)
        us.set_password(ps)
        us.save()
        return True
    else:
        return False

remark_dict = {'Shortage of attendance': 'P', 'Permitted absence in examination':'Ab',
'Unauthorized absence in examination': 'F'}
def student_roll_check(file_name,instructor_obj):

    dict_message={}
    roll_number_error_flag = False
    roll_number_with_error=''

    root_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_dir = os.path.join(root_file,'media','instructor_file')

    excel_test_dir = os.path.join(root_file,'media','test')

    excel_file = file_name
    excel_file_name = os.path.join(excel_test_dir,excel_file)
    print("Check xls",excel_file)

    """
    Check whether file is xls or note
    """
    xlsx_sig = b'\x50\x4B\x05\06'
    xls_sig = b'\x09\x08\x10\x00\x00\x06\x05\x00'
    offset = 512
    size = 8
    print("Helloooooo: ",excel_file_name)

    if (excel_file.endswith(".xlsx") or excel_file.endswith(".xls")):
        print(os.path.exists(excel_file_name))
    else:
        print(os.path.exists(excel_file_name))
        os.remove(excel_file_name)
        dict_message={'reply_code':6,'reply_message':'Please upload xls or xlsx format file.'}
        return dict_message

    try:
        check_instructor = pd.read_excel(excel_file_name,sheet_name = 0,)
    except Exception as e:
        print('Here is the error message: ', e)
        dict_message={'reply_code':6,'reply_message':'Dont put space in file name.'}
        return dict_message

    print("Roll number check is happening ",excel_file_name )
    sem_id = check_instructor.iloc[0,0]
    course_id = check_instructor.iloc[0,1]
    course_name = check_instructor.iloc[0,2]
    first_name = check_instructor.iloc[0,3]
    last_name = check_instructor.iloc[0,4]
    final_file_name = course_id+"_"+sem_id

    try:
        print("first_name= ",first_name,"last_name= ",last_name," course_id= ",course_id," course_name= ", course_name)

        instructor_exists = Course.objects.filter(
            instructor_course=(Instructor.objects.get(user = instructor_obj)),
            sem_id = sem_id,
            course_id = course_id,
            ).exists()
    except Exception as e:
        print('Here is the error message: ', e)
        dict_message={'reply_code':4,'reply_message':""}
        dict_message['reply_message'] = check_semester_course(instructor_obj,sem_id,course_id)
        os.remove(excel_file_name)
        return dict_message

    if(instructor_exists):
        course_obj = Course.objects.get(course_id = course_id)

        marks = pd.read_excel(os.path.join(excel_test_dir,excel_file),sheet_name = 1,)

        if not(check_int_not_empty(marks.iloc[0,3], 0)):
            dict_message={'reply_code':4,'reply_message':"Enter the Mid term marks at D2 properly."}
            return dict_message
        if not(check_int_not_empty(marks.iloc[0,4],0)):
            dict_message = {'reply_code':4,'reply_message':"Enter the End term marks at E2 properly."}
            return dict_message
        if not(check_int_not_empty(marks.iloc[0,5],0)):
            dict_message = {'reply_code':4,'reply_message':"Enter the Practical marks at F2 properly."}
            return dict_message

        mid_term_temp = (check_int_not_empty(marks.iloc[0,3], 0)
        and (type(marks.iloc[0,3]) != str))
        end_term_temp = (check_int_not_empty(marks.iloc[0,4],0)
        and (type(marks.iloc[0,4]) != str))
        practical_temp = (check_int_not_empty(marks.iloc[0,5],0)
        and (type(marks.iloc[0,5]) != str))
        print("Check the boolean value ",mid_term_temp, end_term_temp, practical_temp)

        if mid_term_temp:
            mid_term = marks.iloc[0,3]
        if end_term_temp:
            end_term = marks.iloc[0,4]
        if practical_temp:
            practical_term = marks.iloc[0,5]

        for i in range(1,marks.shape[0]):
            each_student = marks.iloc[i,:]
            roll = each_student[1]

            attendance = each_student[6]
            remarks = each_student[7]
            print("Here are the remarks: ",remarks," boolean: ", pd.isnull(remarks), " ", remarks=="nan", )
            roll_number_individual_flag = False
            if (not(Student.objects.filter(roll_no = roll).exists())
            or not(check_int_not_empty(attendance, 2))
            ):
                roll_number_individual_flag = True
            else:
                if mid_term_temp:
                    print("In mid")
                    student_mid_term = each_student[3]
                    if not(check_int_not_empty(student_mid_term, 1, mid_term)):
                        roll_number_individual_flag = True

                if end_term_temp:
                    print("In End")
                    student_end_term = each_student[4]
                    if not(check_int_not_empty(student_end_term, 1, end_term)):
                        roll_number_individual_flag = True

                if practical_temp:
                    print("In practical")
                    student_practical = each_student[5]
                    if not(check_int_not_empty(student_practical, 1, practical_term)):
                        roll_number_individual_flag = True

                if not pd.isnull(remarks):
                    if not (remarks.lower() in map(str.lower, remark_dict.keys())):
                        roll_number_individual_flag = True

            if (roll_number_individual_flag):
                roll_number_error_flag = True
                roll_number_with_error = roll+", "+roll_number_with_error

        if(roll_number_error_flag):
            os.remove(excel_file_name)
            final_error_rolls="Error in row having roll number: "+roll_number_with_error
            dict_message={'reply_code':2,'reply_message':final_error_rolls}
            return dict_message

        final_file_name = final_file_name+".xlsx"
        try:
            if(os.path.exists(os.path.join(root_file,'media','approved',(final_file_name)))):
                dict_message={'reply_code':5,'reply_message':'You have already uploaded this file once which is approved by HOD'}

            else:
                os.rename(os.path.join(excel_test_dir,excel_file), os.path.join(excel_dir,(final_file_name)))
                dict_message={'reply_code':1,'reply_message':final_file_name}

            return dict_message
        except Exception as e:
            print(e)
            os.remove(excel_file_name)
            dict_message={'reply_code':5,'reply_message':'You have already uploaded this file once'}
            return dict_message
    else:
        dict_message={'reply_code':4,'reply_message':""}
        dict_message['reply_message'] = check_semester_course(instructor_obj,sem_id,course_id)
        os.remove(excel_file_name)
        # dict_message={'reply_code':4,'reply_message':'Details in sheets one is not correct.'}
        return dict_message


'''
check_access == 0 Only check whether E2,D2 and F2 are proper or note
check_access == 1 Check the each value for student
check_access == 2 check absent and present
'''
def check_int_not_empty(val, check_access, total_marks = None):
    print("Here is the val: ",val,"  ", type(val))
    if check_access == 0:
        if (type(val) == np.float64 or type(val) == np.int64 or
        type(val) == int or type(val) == float):
            if np.isnan(val):
                return False
            else:
                return True
        else:
            if (val.replace(" ", "")).lower() == "no":
                return True
            return False

    elif check_access == 1:
        if (type(val) == np.float64 or type(val) == np.int64 or
        type(val) == int or type(val) == float):
            if np.isnan(val):
                return False
            else:
                if  val > total_marks or val < 0 :
                    return False
                else:
                    return True
        else:
            if (val.replace(" ", "")).lower() == "absent":
                return True
            return False
    elif check_access == 2:
        if val == 1 or val == 0:
            return True
        else:
            return False


def check_semester_course(instructor_obj,sem_id,course_id):
    sem_course_message=""
    count = 0
    if (Course.objects.filter(
        instructor_course=(Instructor.objects.get(user = instructor_obj)),
        sem_id = sem_id,
        ).exists()):
        pass
    else:
        count = count+1
        sem_course_message = sem_course_message+"Semester ID "
    if (Course.objects.filter(
        instructor_course=(Instructor.objects.get(user = instructor_obj)),
        course_id = course_id,
        ).exists()):
        pass
    else:
        if count==0:
            sem_course_message = sem_course_message+"Course ID "
        else:
            sem_course_message = sem_course_message+"and Course ID "
    sem_course_message = sem_course_message+"is incorrect in sheetone."

    return sem_course_message

def add_multiple_course_function(course_upload):
    reponse_message={'course_added':[],'course_error':[]}
    for i in range(course_upload.shape[0]):
        each_course = course_upload.iloc[i,:]
        instructor_mail = each_course[0]
        sem_id = each_course[1]
        course_id = each_course[2]
        course_name = each_course[3]
        course_description = each_course[4]
        course_credit = each_course[5]
        print(isinstance(course_credit, str))

        if(get_user_model().objects.filter(email = str(instructor_mail)).exists()):
            if(Course.objects.filter(sem_id = sem_id,course_id = course_id)):
                message_dict={'course_id':course_id ,'sem_id':sem_id,
                'error_message':'Course and sem are already added.'}

                reponse_message['course_error'].append(message_dict)

            else:
                try:
                    user_obj = Instructor.objects.get(user = get_user_model().objects.get(email = str(instructor_mail)))

                    cc= Course.objects.create(instructor_course = user_obj,
                        sem_id = sem_id,
                        course_id = course_id,
                        course_name = course_name,
                        course_description = course_description,
                        credit = course_credit)
                    cc.save()
                    message_dict={'course_id':course_id ,'sem_id':sem_id,
                    'error_message':'Succesfully Saved'}

                    reponse_message['course_added'].append(message_dict)
                except Exception as e:
                    message_dict={'course_id':course_id ,
                    'sem_id':sem_id,
                    'error_message':'Error saving this data'}

                    reponse_message['course_error'].append(message_dict)
                    print('Here is an error: ',e)
        elif(not hf.is_email(instructor_mail)):

            message_dict={'course_id':course_id ,'sem_id':sem_id,
            'error_message':'Email is not proper.'}
            reponse_message['course_error'].append(message_dict)
        else:
            message_dict={'course_id':course_id ,'sem_id':sem_id,
            'error_message':'Instructor does not exist with this mail id.'}

            reponse_message['course_error'].append(message_dict)
        # print(roll_number," ", first_name," ",last_name," ", email, " ", passwords," ")
    return reponse_message


def get_result(user_obj):
    std_course = Course.objects.filter(result__student = Student.objects.get(user = user_obj))
    std_list = list(std_course.values('sem_id','course_id','course_name'))
    student_result_dic=[]
    total_grade = 0
    total_credit = 0
    for i in range(len(std_course)):
        std_course_name = std_list[i]['course_name']
        std_sem_id = std_list[i]['sem_id']
        std_course_id = std_list[i]['course_id']
        couse_obj = Course.objects.get(sem_id = std_sem_id,course_name= std_course_name)
        query_result = Result.objects.filter(
                        student = Student.objects.get(user = user_obj),
                        student_course = couse_obj).values('grade','remark')

        # query_result = Result.objects.filter(
        #                 student = Student.objects.get(user = user_obj),
        #                 student_course = Course.objects.get(sem_id = std_sem_id,course_name= std_course_name)).values('grade')
        print(couse_obj.credit)
        total_credit = total_credit+int(couse_obj.credit)
        total_grade = total_grade+(int(query_result[0]['grade'])*int(couse_obj.credit))
        dict={'sem_id':std_sem_id,'course_name':std_course_name,'std_grade':query_result[0]['remark'],'course_id':std_course_id}
        student_result_dic.append(dict)

    if(len(std_course)>0):
        student_result_dic.append({'total_cgpa':str(total_grade / total_credit)})

    return student_result_dic


def marks_upload(file_name):
    try:
        root_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        excel_dir = os.path.join(root_file,'media','instructor_file')
        approved = os.path.join(root_file,'media','approved')
        excel_file = file_name
        os.rename(os.path.join(excel_dir,excel_file),os.path.join(approved,excel_file))
        print("Helloooooo")
        tt = TempFile.objects.get(file_name = file_name, file_rejected = False)

        tt.file_path = os.path.join('approved',file_name)
        tt.save()
    except Exception as e:
        print(e)
        return False
    try:
        root_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        excel_dir = os.path.join(root_file,'media','instructor_file')
        approved = os.path.join(root_file,'media','approved')
        print(excel_dir)
        excel_file = file_name
        check_instructor = pd.read_excel(os.path.join(approved,excel_file),sheet_name = 0,)
        course_id = check_instructor.iloc[0,1]
        course_obj = Course.objects.get(course_id = course_id)
        print("marks start")
        marks = pd.read_excel(os.path.join(approved,excel_file),sheet_name = 1,)
        print("mark uploads",marks.shape[0],' ',marks.shape[1])

        mid_term_temp = (check_int_not_empty(marks.iloc[0,3], 0)
        and (type(marks.iloc[0,3]) != str))
        end_term_temp = (check_int_not_empty(marks.iloc[0,4],0)
        and (type(marks.iloc[0,4]) != str))
        practical_temp = (check_int_not_empty(marks.iloc[0,5],0)
        and (type(marks.iloc[0,5]) != str))

        print("Check boolean: ",mid_term_temp," ",end_term_temp," ",practical_temp)
        total_mark = 0
        if mid_term_temp:
            total_mark = marks.iloc[0,3]
        if end_term_temp:
            total_mark = total_mark + marks.iloc[0,4]
        if practical_temp:
            total_mark = total_mark + marks.iloc[0,5]

        for i in range(1, marks.shape[0]):
            print("one")
            each_student = marks.iloc[i,:]
            print(each_student)
            roll = each_student[1]
            # print(roll)
            student_attendance = each_student[6]
            remarks = each_student[7]

            stud_obj = Student.objects.get(roll_no = roll)
            print(i,'save')
            student_total_mark = 0
            student_mid = None
            student_end = None
            student_practical = None

            if mid_term_temp:
                student_mid = each_student[3]
                if type(student_mid) == str :
                    stud_add_mid = 0
                else:
                    stud_add_mid = student_mid
                student_total_mark = stud_add_mid

            if end_term_temp:
                student_end = each_student[4]
                if type(student_end) == str:
                    stud_add_end = 0
                else:
                    stud_add_end = student_end
                student_total_mark = student_total_mark + stud_add_end

            if practical_temp:
                student_practical = each_student[5]
                if type(student_practical) == str:
                    stud_add_prac = 0
                else:
                    stud_add_prac = student_practical
                student_total_mark = student_total_mark + stud_add_prac

                # student_total_mark = stud_add_mid + stud_add_end + stud_add_prac
            student_percentage =  (student_total_mark/total_mark)*100
            student_grade = student_percentage/10
            stud_remarks = get_remark(remarks, student_grade)

            Res = Result(student = stud_obj,
            student_course = course_obj,
            mid_term = student_mid, end_term = student_end,
            practical = student_practical,
            attendance = student_attendance,
            total_mark = student_total_mark,
            grade = student_grade,
            mark_percentage = student_percentage,
            remark = stud_remarks)
            Res.save()

            print("save3")
        return True
    except Exception as e:
        print("Error in saving: ",e)
        return False

def get_remark(remarks, student_grade):
    if pd.isnull(remarks):
        if student_grade >= 5:
            resp_remark = 'S'
        else:
            resp_remark = 'US'
    else:
        for k, v in remark_dict.items():
            if remarks.lower() == k.lower():
                resp_remark = v
            else:
                resp_remark = "error in remarks"
    return resp_remark



def download_result_function(user_obj):
    if True:
        doc = SimpleDocTemplate("media/test/"+str(user_obj.first_name)+"_result.pdf", pagesize = A4, rightMargin = 30,leftMargin = 30, topMargin = 30,bottomMargin = 18)
        doc.pagesize = landscape(A4)
        elements = []
        result_lable=[]
        std_result = get_result(user_obj)

        #TODO: Get this line right instead of just copying it from the docs
        style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                               ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                               ('VALIGN',(0,0),(0,-1),'TOP'),
                               ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                               ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                               ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                               ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ])
        style_para = ParagraphStyle(
                name='Normal',
                fontName='Times-Bold',
                fontSize = 14,
            )

        logo = os.path.join('media','pdf_logo.png')

        # We really want to scale the image to fit in a box and keep proportions.
        im = Image(logo)
        elements.append(im)
        elements.append(Spacer(1, 0.25*inch))

        user_str='Hello '+str(user_obj.first_name)
        elements.append(Paragraph(user_str,style = style_para))
        elements.append(Spacer(1, 0.25*inch))


        for ky in std_result[0].keys():
            result_lable.append(ky)

        data = [result_lable]
        result_value=[]
        print(len(std_result))
        for ind in range(len(std_result)):
            if(ind!=len(std_result)-1):
                print('lenght',len(std_result[ind]))
                for k, v in std_result[ind].items():
                    result_value.append(str(v))
                data.append(result_value)
                result_value=[]
            else:
                data.append([])
                for k, v in std_result[ind].items():
                    result_value.append('Your CGPA is: '+v)
                data.append(result_value)
                result_value=[]
        print("Data: ",data)


        #Configure style and word wrap
        s = getSampleStyleSheet()
        s = s["BodyText"]
        s.wordWrap = 'CJK'
        data2 = [[Paragraph(cell, s) for cell in row] for row in data]
        t = Table(data2)
        t.setStyle(style)

        #Send the data and build the file
        elements.append(t)
        doc.build(elements)
        return True
    else:
        return False

def add_file_to_instructor(user_obj,file_pk):
    try:
        instructor_obj = get_object_or_404(Instructor, user = user_obj)
        instructor_obj.intructor_file.add(TempFile.objects.get(id = file_pk))
        return True
    except Exception as e:
        print(e)
        return False


def add_multiple_student_function(student_upload):
    reponse_message={'student_exist':[],'student_added':[],'student_error':[]}
    for i in range(student_upload.shape[0]):
        each_student = student_upload.iloc[i,:]
        roll_number = each_student[0]
        first_name = each_student[1]
        last_name = each_student[2]
        email = each_student[3]
        passwords = each_student[4]
        if(get_user_model().objects.filter(email = str(email)).exists()):
            reponse_message['student_exist'].append(email)
        else:
            try:
                if (is_email(email)):
                    cc = get_user_model().objects.create_user(
                    email,passwords)
                    cc.first_name = first_name
                    cc.last_name = last_name
                    cc.save()

                    st = Student(user = cc,
                    roll_no = roll_number,
                    degree_type='BTech'
                    )
                    st.save()
                    reponse_message['student_added'].append(email)
                else:
                    reponse_message['student_error'].append(email)

            except Exception as e:
                reponse_message['student_error'].append(email)
                print('Here is an error: ',e)

        print(roll_number," ", first_name," ",last_name," ", email, " ", passwords," ")
    return reponse_message

def is_email(string):
    validator = EmailValidator()
    try:
        validator(string)
    except ValidationError:
        return False
    return True

def random_name():
    min_char = 8
    max_char = 12
    allchar = string.ascii_letters + string.digits
    random_name = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
    return random_name
