from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import CustomUser
from .serializers import UserSerializer
from .utils import encode_jwt
from .tasks import send_mail_func
import json



class RegisterUser(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            if CustomUser.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

            # Create user with validated data
            user = CustomUser.objects.create_user(
                name=serializer.validated_data['name'], 
                email=serializer.validated_data['email'], 
                password=serializer.validated_data['password']
            )
            send_mail_func.delay(serializer.validated_data['email'])
            user.save()

            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    def get(self, request):
        return Response({"message": "Get method not allowed!"}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"message": "Login successful", "token": token}, status=status.HTTP_200_OK)

        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
