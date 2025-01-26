from django.urls import path

from . import views

urlpatterns = [
    path('',views.home),
    path('add-post/',views.add),
    path('user-profile/<str:pk>/',views.user_profile,name='user-profile'),
    path('full-post/<str:pk>',views.posts_full,name='full-post'),
    path('delete-comment/<str:pk>',views.deletecomment,name='delete-comment'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('register/',views.register,name='register'),
    
]
