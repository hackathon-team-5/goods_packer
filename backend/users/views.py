from core.pagination import CustomPaginator
from core.utils import key_generator
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .serializers import SetPasswordSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """
    Users:
    - `GET`: list of users
    - `POST`: users registration
    - `GET`: user profile by id
    - `GET`/me/: current user
    - `POST`/set_password/: password change
    """
    permission_classes = (DjangoModelPermissions,)
    pagination_class = CustomPaginator

    def perform_create(self, serializer: Serializer) -> None:
        """
        Creates a new user and saves it to the database.
        """
        serializer.is_valid(raise_exception=True)
        who = key_generator(32)
        user = serializer.save(who=who)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=('POST',), detail=False,
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        """
        Changes the user's password.
        """
        serializer = SetPasswordSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(
            {'detail': 'Пароль успешно изменен!'},
            status=status.HTTP_204_NO_CONTENT
        )
