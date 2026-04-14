from django.urls import path
from .views import  LoginView, questions, results,TechnologyList,RegisterView,PasswordResetRequestView, SetNewPasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
     path('forgot-password/', PasswordResetRequestView.as_view()),
    path('reset-password/<uidb64>/<token>/', SetNewPasswordView.as_view()),
    path('questions/', questions.as_view(), name='questions'),
    path('technologies/',TechnologyList.as_view()),
    path("register/",RegisterView.as_view()),
    path('results/', results.as_view(), name='results'),
]