from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect


# Create your views here.
def register(request):
    SpecialSym = ['$', '@', '#', '%', '!']
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('register')
        if not username.isalnum():
            messages.error(request, "Username must only have alphanumeric characters")
            return redirect('register')
        if len(password1) < 8:
            messages.error(request, "Password should be more 8 characters")
            return redirect('register')
        if not any(char.isdigit() for char in password1):
            messages.error('Password should have at least one numeral')
            return redirect('register')
        if not any(char.isupper() for char in password1):
            messages.error('Password should have at least one Uppercase letter')
            return redirect('register')
        if not any(char.islower() for char in password1):
            messages.error('Password should have at least one Lowercase letter')
            return redirect('register')
        if not any(char in SpecialSym for char in password1):
            messages.error('Password should have at least one of the symbols !$@#')
            return redirect('register')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,
                                                password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                print('User Created')
                return redirect('login')
        else:
            messages.info(request, 'password not matching')
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print('User Verified')
            return redirect('/')
        else:
            messages.info(request, 'Invalid User Name or Password')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')