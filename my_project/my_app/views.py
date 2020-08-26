from django.shortcuts import render, redirect
from .models import AiClass, AiStudents
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

ERROR_MSG = {
    'ID_EXIST':'이미사용중',
    'ID_NOT_EXIST':'존재하지 않는 아이디',
    'ID_PW_MISSING' : '아이디와 비번 확인좀',
    'PW_CHECK' :'비밀번호가 일치 X'
}

def home(request):

    class_object = AiClass.objects.all()

    return render(request, 'home.html',{'class_object':class_object})

def detail(request, class_num):
    print('==========================',class_num)

    class_obj = AiClass.objects.get(class_num=class_num)
    student_obj = AiStudents.objects.filter(class_num = class_num)

    context = {
        'class_obj':class_obj,
        'student_obj':student_obj
    }

    return render(request, 'detail.html', context)

def add(request, class_num):
    class_obj = AiClass.objects.get(class_num = class_num)

    print('==================',request.POST)

    if request.method == 'POST':

        AiStudents.objects.create(
            class_num = class_num,
            name = request.POST['name'],
            phone_num = request.POST['phone']
        )

        return redirect('detail', class_num)

    context = {
        'class_obj':class_obj
    }

    return render(request, 'add.html', context)

def student(request, student_pk):
    student = AiStudents.objects.get(pk=student_pk)
    context = {
        'student':student
    }
    return render(request, 'student.html',context)

def edit(request, student_pk):

    if request.method == 'POST':
    
        AiStudents.objects.filter(pk=student_pk).update(
            name = request.POST['name'],
            phone_num = request.POST['phone_num']
        )

        return redirect('student', student_pk)

    student = AiStudents.objects.get(pk = student_pk)
    context = {
        'student':student
    } 
    return render(request, 'edit.html', context)

def delete(request, class_num, student_pk):
    target_student = AiStudents.objects.get(pk = student_pk)
    target_student.delete()

    return redirect('detail', class_num)

def signup(request):

    context = {
        'error':{
            'state':False,
            'msg':''
        }
    }

    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_pw_check = request.POST['user_pw_check']

        if (user_id and user_pw):

            user = User.objects.filter(username=user_id)

            if len(user) == 0:

                if user_pw == user_pw_check :
                    # 회원 등록
                    created_user = User.objects.create_user(
                        username = user_id,
                        password = user_pw
                    )

                    auth.login(request,created_user)

                    return redirect('home')

                else :                
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_EXIST']
        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'signup.html',context)

def login(request):
    context = {
        'error':{
            'state':False,
            'msg':''
        }
    }
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']

        user = User.objects.filter(username=user_id)

        if (user_id and user_pw):
            if len(user) != 0:

                login_user = auth.authenticate(
                    username = user_id,
                    password = user_pw
                )
                if user != None:
                    auth.login(request,login_user)
                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_NOT_EXIST']
        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'login.html',context)

def logout(request):
    auth.logout(request)
    return redirect('home')