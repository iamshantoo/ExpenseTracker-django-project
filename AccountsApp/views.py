from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserProfileChange, ProfilePic
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models.query_utils import Q
# Create your views here.


def RegistrationView(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Account Created Successfully.")

            # auto login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            new_user = authenticate(username=username, password=password)
            login(request, new_user)

            # sending welcoming email

            subject = 'Expense Tracker Registration Successful'
            body = render_to_string('intro_email.html')

            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [new_user.email]
            )
            return HttpResponseRedirect(reverse('AccountsApp:login_view'))
    dict = {'form': form}
    return render(request, 'registrationPage.html', context=dict)


def LoginView(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('AccountsApp:profile_view'))
    return render(request, 'loginPage.html', context={'form': form})


@login_required
def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('ExpenseApp:home_page'))


@login_required
def profile(request):
    return render(request, 'profile.html', context={})


@login_required
def user_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)
    return render(request, 'change_profile.html', context={'form': form})


@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'pass_change.html', context={'form': form, 'changed': changed})


@login_required
def add_pro_pic(request):
    form = ProfilePic()
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('AccountsApp:profile_view'))
        else:
            return HttpResponseRedirect(reverse(''))
    return render(request, 'pro_pic_add.html', context={'form': form})


@login_required
def change_pro_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES,
                          instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('AccountsApp:profile_view'))
    return render(request, 'pro_pic_add.html', context={'form': form})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Expense Tracker',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return HttpResponseRedirect(reverse('AccountsApp:password_reset_done'))
    password_reset_form = PasswordResetForm()
    return render(request, 'password_reset.html', context={"password_reset_form": password_reset_form})
