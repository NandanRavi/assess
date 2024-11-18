from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Message
from users.models import CustomUser
from .serializers import MessageSerializer

class ChatHistoryView(APIView):

    def get(self, request, receiver_email):
        if not request.user.is_authenticated:
            return Response({"error":"Login User"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            receiver = CustomUser.objects.get(email=receiver_email)
            messages = Message.objects.filter(
                (Q(sender=request.user) & Q(receiver=receiver)) |
                (Q(sender=receiver) & Q(receiver=request.user))
            ).order_by('timestamp')
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=200)
        except CustomUser.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)
