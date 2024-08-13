from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from . models import extended, StockImage
from django import forms
# Create your views here.

class StockImageForm(forms.ModelForm):
    class Meta:
        model = StockImage
        fields = ['title', 'description', 'image']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = extended
        fields = ['img']
def main(requests):
    images = StockImage.objects.all()
    return render(requests, 'main.html', {'images': images})

def user_login(requests):
    if requests.method == 'POST':
        u = requests.POST['u']
        p = requests.POST['p']
        us = authenticate(requests, username=u, password=p)
        if us is not None:
            auth_login(requests,us)
            return render(requests, 'main.html')
        else:
            return render(requests, '', {'message': 'Something Went Wrong, Try Agian'})
    return render(requests, 'login.html')

def signup(requests):
    if requests.method == 'POST':
        u = requests.POST['u']
        f = requests.POST['f']
        l = requests.POST['l']
        e = requests.POST['e']
        p = requests.POST['p']
        i = requests.FILES['i']
        us = User.objects.create_user(username=u, first_name=f, last_name=l, password=p, email=e, is_active=False)
        try:
            us.save()
            ex = extended()
            ex.id = us
            ex.img = i
            ex.save()
            link = f'http://127.0.0.1:8000/activate/{us.pk}/'
            em = EmailMessage('Account activation','Thank you for registering please click this link to activate your account ' + link,'retakebyib@gmail.com',[e])
            em.send()
            return redirect('login')
        except:
            return render(requests, 'signup.html',{'mes':'Something Went Wrong'})
    return render(requests, 'signup.html')

@login_required(login_url='accounts/login/')
def upload_image(requests):
    if requests.method == 'POST':
        form = StockImageForm(requests.POST, requests.FILES)
        if form.is_valid():
            stock_image = form.save(commit=False)
            stock_image.user = requests.user
            stock_image.save()
            return redirect('main')
    else:
        form = StockImageForm()
    return render(requests, 'upload_image.html', {'form': form})

@login_required(login_url='accounts/login/')
def user_dashboard(requests):
    if requests.method == 'POST':
        user_form = UserUpdateForm(requests.POST, instance=requests.user)
        profile_form = ProfileUpdateForm(requests.POST, requests.FILES, instance=requests.user.extended)
        if 'update' in requests.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('user_dashboard')
        elif 'delete' in requests.POST:
            return redirect('delete_user')
    else:
        user_form = UserUpdateForm(instance=requests.user)
        profile_form = ProfileUpdateForm(instance=requests.user.extended)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(requests, 'dashboard.html', context)

def aboutus(requests):
    return render(requests, 'aboutus.html')

def contactus(requests):
    return render(requests, 'contactus.html')

@login_required(login_url='accounts/login/')
def download_image(request, image_id):
    image = get_object_or_404(StockImage, id=image_id)
    image_path = image.image.path

    with open(image_path, 'rb') as img:
        response = HttpResponse(img.read(), content_type="image/jpeg")
        response['Content-Disposition'] = f'attachment; filename="{image.title}.jpg"'
        return response

@login_required(login_url='accounts/login/')
def delete_user(requests):
    if requests.method == 'POST':
        user = requests.user
        logout(requests)
        user.delete()
        return redirect('main')
    return render(requests, 'delete_user.html')

@login_required(login_url='accounts/login/')
def user_logout(requests):
    try:
        logout(requests)
    except:
        ...
    return render(requests, 'main.html')

def activate(requests,id):
    u = User.objects.get(pk = id)
    u.is_active = True
    u.save()
    return render(requests,'login.html')