"""AAU_v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from app_aau import views

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views
admin.site.site_header = 'AAU administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.IndexPage.as_view(), name='index'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/',views.pass_change,name='change_password'),
#
    path('instructor_file/',views.InstructorFileUpload.as_view(), name='instructor_file_upload'),
    path('view_uploaded_file/',views.View_Uploaded_File.as_view(), name='view_file_upload'),

    path('add_multiple_course/',views.add_multiple_course,name='add_multiple_course'),
    path('view_template/',views.template_page,name='view_template'),
    path('instructor_upload_message/<upload_message>',views.FileUploadMessage, name='instructor_upload_message'),
    path('approved_by_hod/',views.approved_marks_by_hod, name='approved_by_hod'),
    path('approve_marks_dean/',views.approve_marks_dean, name='approve_marks_dean'),
    path('approve_marks_registrar/',views.approve_marks_registrar, name='approve_marks_registrar'),
#
    path('reject_marks_file/',views.rejected_marks_file, name='reject_marks_file'),
    path('reject_marks_reason/',views.reject_marks_reason, name='reject_marks_reason'),
#
    path('student_result/',views.StudentResult.as_view(), name='student_result'),
    path('release_marks/',views.release_marks, name='release_marks'),
#
# ################
#
    path('download/<fileName>/',views.file_download,name='downloadFile'),
#
# ##############
#
#
    path('result_download/',views.download_result,name='result_download'),
#
# ##################
#
    path('add_multiple_student/',views.add_multiple_student,name='add_multiple_student'),
#
    path('view_template/',views.template_page,name='view_template'),
    path('template_download/<fileName>/',views.template_download,name='template_download'),
#


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIR)
