from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import User_detail, Media
from django.contrib.auth.decorators import login_required
import pickle
import os
from PIL import Image
import numpy as np
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from datetime import datetime

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('sign_up')

        # Create user
        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name)

        # Create patient profile
        user_detail = User_detail.objects.create(user=user,
                                        address_line1=address_line1, city=city, state=state, pincode=pincode, phone=phone)
        user_detail.save()

        messages.success(request, "Signup successful!")
        return redirect('home')
    return render(request, 'sign_up.html')

def display_last_image(request):
    last_image = Media.objects.last()
    return render(request, 'index.html', {'last_image': last_image})

def home(request):
    if request.user.is_authenticated:
        if request.method=='POST' and 'imageInput' in request.FILES:
            upload = request.FILES['imageInput']
            media=Media(user=request.user,picture=upload)
            media.save()
            if predict(media.picture)[0][1] > 0.50:
                media.status=True 
                media.save()
            print(media.status)
            user=request.user
            user_detail=User_detail.objects.get(user=user)
            return render(request, 'output.html',{'user':user_detail,'media':media})
        u = User.objects.filter(username=request.user)
        u = u[0]
        return render(request, 'index.html', {'users': u})
    return redirect('sign_in')

def profile(request):
    if request.method == 'POST':
        # Update User fields
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.username = request.POST.get('username', user.username)
        user.save()

        # Update UserDetail fields
        user_detail = user.user_detail  # Assuming OneToOne relationship
        user_detail.phone = request.POST.get('phone', user_detail.phone)
        user_detail.address_line1 = request.POST.get('address', user_detail.address_line1)
        user_detail.city = request.POST.get('city', user_detail.city)
        user_detail.state = request.POST.get('state', user_detail.state)
        user_detail.pincode = request.POST.get('pincode', user_detail.pincode)
        user_detail.save()

        return redirect('profile')  # Redirect to the profile page after saving

    # For GET request, render the profile template
    user=request.user
    user_detail=User_detail.objects.get(user=user)
    return render(request, 'profile.html',{'user':user_detail})

def logout(request):
    auth.logout(request)
    return redirect('sign_in')

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user is linked to a Patient instance
            return redirect('home')
            # Check if the user is linked to a Doctor instance
        else:
            messages.error(request, "Invalid username or password")
            return redirect('sign_in')
    return render(request, 'sign_in.html')

def predict(img):
    pwd = os.path.dirname(__file__)
    pickled_model=pickle.load(open(pwd+'/model.pkl','rb'))
    image_size = (64, 64)
    img = Image.open('C:/Users/synam/Desktop/Final_Project(5th Sem)/govhelp'+img.url).convert("RGB")
    img = img.resize(image_size)
    img_array = np.array(img) / 255.0
    li=[]
    li.append(img_array)
    li=np.array(li)
    return pickled_model.predict(li)

def generate_pdf(request):
    user = request.user
    profile = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.user_detail.phone,
        'address_line1': user.user_detail.address_line1,
        'city': user.user_detail.city,
        'state': user.user_detail.state,
        'pincode': user.user_detail.pincode,
        'date': datetime.now().strftime('%B %d, %Y')
    }
    html_content = render_to_string('pdf_template.html', {'profile': profile})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Acknowledgement Letter.pdf"'
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response
