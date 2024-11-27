from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from myapp.serializers.userSerializer import UserCreateSerializer, UserSerializer  # Import the appropriate serializers
from myapp.permissions import IsAdminOrOwner
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class UserViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminOrOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAdminOrOwner]
        return super().get_permissions()

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)  # Use a serializer to serialize the QuerySet
        return Response(serializer.data)  # Return the serialized data

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(request, user)
            serializer = UserSerializer(user)  # Serialize the user object
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(request, user)
            serializer = UserCreateSerializer(user, data=request.data, partial=True)  # Correct this line
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(request, user)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(request, user)
            
            # Check if the request is to change the user's admin status
            if request.user.is_staff and 'is_staff' in request.data:
                if request.data['is_staff'] and not request.user.is_superuser:
                    return Response({'detail': 'Only superusers can grant admin privileges.'}, status=status.HTTP_403_FORBIDDEN)
            
            # Perform the partial update
            serializer = UserCreateSerializer(user, data=request.data, partial=True)  # Correct this line
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)