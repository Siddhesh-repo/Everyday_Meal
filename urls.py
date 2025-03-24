from django.urls import path
from . import views  

urlpatterns=[

    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('receipes/',views.receipes,name='receipes'),  
    path('delete_receipe/<id>/',views.delete_receipe,name='delete_receipe'),
    path('update_receipe/<id>/',views.update_receipe,name='update_receipe'),

]