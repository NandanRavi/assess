from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from .serializers import UserSerializer
from .utils import encode_jwt
from .tasks import send_mail_func
import json

class UserView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class RegisterUser(APIView):
        def get(self, request):
            return Response({"message":"Get Method Not allowed!!!"}, status=status.HTTP_400_BAD_REQUEST)
    
        def post(self, request):
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                if CustomUser.objects.filter(email=serializer.validated_data['email']).exists():
                    return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)
                user = serializer.save()
                send_mail_func.apply_async(args=[user.email])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    def get(self, request):
        return Response({"message":"Get Method Not allowed!!!"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return Response({"error": "Email and Password are required"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            token = encode_jwt(user)
            login(request, user)
            return Response({'message': 'Logged in successfully', "user":f"{user}", "token":token}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUserView(APIView):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return Response({"message":"Please Login1!!"}, status=status.HTTP_401_UNAUTHORIZED)
            logout(request)
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_400_BAD_REQUEST)