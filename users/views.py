from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserRegisterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.

    The queryset is all users in the system.
    The serializer class is UserSerializer.
    The permission class is AllowAny for the create action (registering a new user)
    and IsAdminUser for the rest of the actions (viewing, editing, deleting a user).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
