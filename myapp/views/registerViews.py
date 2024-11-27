# views/register_views.py
from django.core.mail import send_mail
from django.conf import settings
# views/register_views.py
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers.userSerializer import UserCreateSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Send a welcome email
        send_mail(
            'Welcome to Our Site',
            'Thank you for registering. Your account has been created successfully.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
