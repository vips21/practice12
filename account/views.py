from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.contrib.auth import login
from .forms import UserCreateForm, UserLoginForm, UserFilesForm, \
    FileCommentsForm, UserEmailForm
from .models import User, UserEmail, FileComments, UserFiles


def get_client_ip(request):
    '''
    To get ip of user
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def sign_up(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.ip_address = get_client_ip(request)
            user.save()
            login(request, user)
            UserEmail.objects.create(
                user = user,
                email = user.email,
                primary = True
            )
            return redirect("home")
        else:
            for msg in form.errors:
                messages.error(request, form.errors[msg])    
    form = UserCreateForm()
    return render(request, 'account/register.html', {'form':form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.filter(email__iexact = email).first()
        if user and user.is_active and user.check_password(password):
            login(request, user)
            return redirect('home')
        messages.error(request, "Email and password do not match")
    form = UserLoginForm()
    return render(request, 'account/login.html', {'form':form})


@login_required(login_url='/')
def home(request):
    if request.user.is_superuser:
        users = User.objects.all().exclude(id=request.user.id)
        return render(request, 'account/home.html', {'users':users})
    else:
        files = UserFiles.objects.filter(user=request.user)
        emails = UserEmail.objects.filter(user=request.user)
        return render(request, 'account/home.html', {'files':files, 'emails':emails})


def upload_file(request):
    if request.method == 'POST':
        form = UserFilesForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.save(commit=False)
            files.user = request.user
            files.save()
            return redirect('home')
        for msg in form.errors:
                messages.error(request, form.errors[msg])


def user_email(request):
    if request.method == 'POST':
        user = request.user
        form = UserEmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.user = user
            email.save()
            if email.primary:
                user.email = email.email
                user.save()
                UserEmail.objects.exclude(id=email.id).update(primary=False)
        print(form.errors)
        for msg in form.errors:
                messages.error(request, form.errors[msg])
        return redirect('home')                


def file_comment(request, file_id):
    if request.method == 'POST':
        form = FileCommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commented_bye = request.user
            comment.files_id = file_id
            comment.save()
            return redirect('file_comment', file_id=file_id)
        for msg in form.errors:
                messages.error(request, form.errors[msg])
    
    file = UserFiles.objects.filter(id=file_id).first()
    comments = FileComments.objects.all()
    return render(request, 'account/files_comments.html', {'comments':comments, 'file':file})