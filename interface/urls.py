from django.urls import path
from . import views
urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in',views.sign_in, name='sign_in'),
    path('',views.home, name='home'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('upload-image/',views.home,name='upload_image'),
    path('update-profile/',views.profile,name='update_profile'),
    path('pictures/', views.display_last_image, name='display_last_image'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf')
]