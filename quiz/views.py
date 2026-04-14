from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User,Question,Result
from .serializers import QuestionSerializer,ResultSerializer,LoginSerializer,RegisterSerializer,PasswordResetRequestSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

class RegisterView(APIView):
    def post(self, request):
        data = request.data

        
        if User.objects.filter(email=data.get("email")).exists():
            return Response({
                "status": "error",
                "message": "Email already registered"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            
            try:
                send_mail(
                    subject="New Student Registered",
                    message=f"Student {user.first_name} {user.last_name} with email {user.email} has registered.",
                    from_email="vijayakasu9@gmail.com",
                    recipient_list=["vijayakasu9@gmail.com"],
                    fail_silently=False
                )
            except Exception as e:
                print("Email sending failed:", e)

            return Response({
                "status": "success",
                "message": "Registration Successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            }, status=status.HTTP_201_CREATED)

        print("Registration errors:", serializer.errors)
        return Response({
            "status": "error",
            "message": "Registration Failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                return Response({
                    "status":"success",
                    "message":"Login Successful",
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "mobile": user.mobile
                    }
                })
            return Response({"status":"error","message":"Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"status":"error","message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Email not found"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Generate token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        
        reset_link = f"http://127.0.0.1:5173/reset-password/{uid}/{token}"
        print(f"DEBUG: Password reset link generated: {reset_link}")

        
        try:
            send_mail(
                subject="Password Reset Request",
                message=f"Hi {user.first_name},\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you didn't request this, ignore this email.",
                from_email="vijayakasu9@gmail.com",
                recipient_list=[user.email],
                fail_silently=False
            )
        except Exception as e:
            print("Email sending failed:", e)
            return Response({
                "status": "error",
                "message": "Failed to send email"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": "success",
            "message": "Password reset email sent"
        }, status=status.HTTP_200_OK)


class SetNewPasswordView(APIView):
    def post(self, request, uidb64, token):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"status": "error", "message": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"status": "error", "message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response({"status": "success", "message": "Password reset successfully"}, status=status.HTTP_200_OK)

class questions(APIView):
    def get(self, request):
        tech = request.GET.get("technology")

        if tech:
            filtered_questions = Question.objects.filter(Technology__iexact=tech)
        else:
            filtered_questions = Question.objects.all()

        ques_obj = QuestionSerializer(filtered_questions, many=True)
        return Response(ques_obj.data)

    def post(self, request):
        ques_obj = QuestionSerializer(data=request.data)
        if ques_obj.is_valid():
            ques_obj.save()
            return Response(ques_obj.data, status=status.HTTP_201_CREATED)
        return Response(ques_obj.errors, status=status.HTTP_400_BAD_REQUEST)
class QuestionList(APIView):

    def get(self, request):

        tech = request.GET.get('technology')

        if tech:
            questions = Question.objects.filter(Technology=tech)
        else:
            questions = Question.objects.all()

        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data)

class TechnologyList(APIView):
    def get(self, request):
        technologies = Question.objects.values_list('Technology', flat=True).distinct()
        return Response(technologies)


class results(APIView):
    def get(self,request):
        results=Result.objects.all()
        res_obj=ResultSerializer(results,many=True)
        return Response(res_obj.data)
    
    def post(self,request):
        res_obj=ResultSerializer(data=request.data)
        if res_obj.is_valid():
            res_obj.save()
            return Response(res_obj.data,status=status.HTTP_201_CREATED)
        return Response(res_obj.errors,status=status.HTTP_400_BAD_REQUEST)
