# Generated by Django 2.1.1 on 2019-06-19 09:58

import app_aau.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', app_aau.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem_id', models.CharField(max_length=256)),
                ('course_id', models.CharField(max_length=256)),
                ('course_name', models.CharField(max_length=256)),
                ('course_description', models.CharField(max_length=256, null=True)),
                ('credit', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Dean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Department_name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_instructor_hod', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('instructor_department', models.ManyToManyField(to='app_aau.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Registrar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid_term', models.CharField(max_length=20)),
                ('end_term', models.CharField(max_length=20)),
                ('practical', models.CharField(max_length=20)),
                ('attendance', models.CharField(max_length=1)),
                ('total_mark', models.FloatField()),
                ('mark_percentage', models.FloatField()),
                ('grade', models.FloatField()),
                ('remark', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_no', models.CharField(max_length=10)),
                ('degree_type', models.CharField(max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TempFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=256)),
                ('file_path', models.FileField(blank=True, upload_to='test')),
                ('file_uploaded_hod', models.BooleanField(default=False)),
                ('file_uploaded_dean', models.BooleanField(default=False)),
                ('file_uploaded_registrar', models.BooleanField(default=False)),
                ('file_rejected', models.BooleanField(default=False)),
                ('file_status', models.CharField(blank=True, max_length=256)),
                ('marks_release', models.BooleanField(default=False)),
                ('file_rejected_reason', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterOrderWithRespectTo(
            name='tempfile',
            order_with_respect_to='created',
        ),
        migrations.AlterOrderWithRespectTo(
            name='student',
            order_with_respect_to='created',
        ),
        migrations.AddField(
            model_name='result',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_aau.Student'),
        ),
        migrations.AddField(
            model_name='result',
            name='student_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_aau.Course'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='result',
            order_with_respect_to='created',
        ),
        migrations.AddField(
            model_name='instructor',
            name='intructor_file',
            field=models.ManyToManyField(blank=True, null=True, to='app_aau.TempFile'),
        ),
        migrations.AddField(
            model_name='instructor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterOrderWithRespectTo(
            name='instructor',
            order_with_respect_to='created',
        ),
        migrations.AddField(
            model_name='course',
            name='instructor_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_aau.Instructor'),
        ),
    ]