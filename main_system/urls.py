from django.contrib import admin
from django.urls import path, include
from .views import Home, Login, Signup, Logout, borrowers, \
    LenderList, transfer, confirmation, acceptAccount, dashboard, \
    CreateBorrower, CreateLender, DeleteBorrowers, DeleteLender, LenderDetail, about

urlpatterns = [
    path('',Home),
    path('dashboard/', dashboard, name='dashboard'),
    path('about/', about, name='about'),
    path('login/', Login, name='login'),
    path('register/', Signup.as_view(), name='register'),
    path('logout/', Logout, name='logout'),
    path('loan_list/', borrowers.as_view(), name='loan_list'),
    path('lenders_list/', LenderList.as_view(), name='lenders_list'),
    path('transfer/', transfer, name='transfer'),
    path('confirmation/', confirmation ),
    path('acceptAccount/', acceptAccount),
    path('request-loan', CreateBorrower.as_view(), name='CreateBorrower'),
    path('pledge-loan', CreateLender.as_view(), name='CreateLender'),
    path('delete-b', DeleteBorrowers.as_view(), name='DeleteBorrowers'),
    path('delete-l/<int:pk>/', DeleteLender.as_view(), name='DeleteLender'),
    path('loan-details/<int:id>/', LenderDetail, name='LenderDetails'),
]
