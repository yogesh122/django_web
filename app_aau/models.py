from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib import auth
from django.urls import reverse
from django_mysql.models import ListCharField
from django.contrib.auth.models import User
from django.utils import timezone


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Registrar(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name


class Dean(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name

class Department(models.Model):
    Department_name=models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.Department_name

class Student(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    roll_no=models.CharField(max_length=10) #check the roll number exist using query.
    degree_type=models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
   	    order_with_respect_to = 'created'

    def __str__(self):
        return self.roll_no


class TempFile(models.Model):

    file_name=models.CharField(max_length=256)
    file_path=models.FileField(upload_to='test',blank=True)
# File approved by hod
    file_uploaded_hod = models.BooleanField(default=False)
    file_uploaded_dean = models.BooleanField(default=False)
    file_uploaded_registrar = models.BooleanField(default=False)

    file_rejected = models.BooleanField(default=False)
    file_status = models.CharField(max_length=256,blank=True)
    marks_release = models.BooleanField(default=False)
    file_rejected_reason = models.BooleanField(default=False)

    created = models.DateTimeField(default=timezone.now)

    class Meta:
   	    order_with_respect_to = 'created'

    def get_absolute_url(self):
        return reverse('instructor_file_upload')

    def __str__(self):
        return self.file_name

class Instructor(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    instructor_department=models.ManyToManyField(Department)
    intructor_file=models.ManyToManyField(TempFile,null=True,blank=True)
    is_instructor_hod=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
   	    order_with_respect_to = 'created'

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name

class Course(models.Model):
	#Change onetoone to foriegn key
    instructor_course=models.ForeignKey(Instructor,on_delete=models.CASCADE)
    sem_id = models.CharField(max_length=256)
    course_id = models.CharField(max_length=256)
    course_name = models.CharField(max_length=256)
    course_description = models.CharField(max_length=256,null=True)
    credit = models.IntegerField()

    def __str__(self):
        return self.course_id + "-"+self.instructor_course.user.first_name 

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    student_course = models.ForeignKey(Course,on_delete=models.CASCADE)
    mid_term = models.CharField(max_length=20, null = True)
    end_term = models.CharField(max_length=20, null = True)
    practical = models.CharField(max_length=20, null = True)
    attendance = models.CharField(max_length=1)
    total_mark = models.FloatField()
    mark_percentage = models.FloatField()
    grade = models.FloatField()
    remark = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        order_with_respect_to = 'created'

    def __str__(self):
        return str(self.student.roll_no) + ' : ' + str(self.grade)
