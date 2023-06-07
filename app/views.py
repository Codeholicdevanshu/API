from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework.response import Response
from .models import *
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
# Create your views here.


def register(request):
    return render(request,'form.html')

def login(request):
    return render(request,'login.html')

def base(request):
    return render(request,'base.html')

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            firstname = serializer.validated_data['firstname']
            lastname = serializer.validated_data['lastname']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            #fetching data from models
            user = Registeruser(firstname=firstname,lastname=lastname,email=email,password=password)
            if user:
                user.password = make_password(user.password)
                user.save()
                return Response({'message':"User Register Successfully"},status=200)
            else:
                return Response({'error':'invalid data'},status=400)
        
        return Response({'error':'invalid data'} ,status=400)
    
class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user = Registeruser.objects.get(email=email)
                #print(user)

                if user:
                    flag = check_password(password,user.password)
                    if flag:
                        refresh = RefreshToken.for_user(user)
                        return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        })
                    else:
                        return Response({
                            'status':400,
                            'message':'Invalid user please register'

                        })
                else:
                    return Response({
                        'status': 400,
                        'message': 'Invalid credentials',
                        'data': {}
                    })

            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            })
        except Registeruser.DoesNotExist:
            return Response({
                'status': 400,
                'message': 'User not registered',
                'data': {}
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal server error',
                'data': str(e)
            })


            





