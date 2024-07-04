import random
from string import digits

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from .permissions import IsAdminUser
from .serializers import (
    GetTokenSerializer,
    UserCreateSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Генерация кода подтверждения
    # Если в настройках стоит использовать фиксированный код, то
    # его не нужно пересохранять в коллекции postman во время тестов.
    if settings.USE_FIXED_CONFIRMATION_CODE:
        confirmation_code = settings.FIXED_CONFIRMATION_CODE
    else:
        confirmation_code = ''.join(random.choices(digits, k=5))

    # Сохранение пользователя с кодом подтверждения
    serializer.save(confirmation_code=confirmation_code)

    # Получение объекта пользователя
    user = User.objects.get(username=serializer.validated_data['username'])

    # Отправка письма с кодом подтверждения
    send_confirmation_email(user, confirmation_code)

    return Response(serializer.data, status=status.HTTP_200_OK)


def send_confirmation_email(user, confirmation_code):
    subject = 'Код подтверждения для YaMDb'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data.get('confirmation_code')

    user = get_object_or_404(
        User, username=serializer.validated_data.get('username')
    )
    if (
        user.confirmation_code != confirmation_code
        or user.confirmation_code == 0
    ):
        return Response(
            {'detail': 'Invalid confirmation code'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user.confirmation_code = 0
    user.save()
    token = AccessToken.for_user(user)

    return Response({'token': str(token)}, status=status.HTTP_200_OK)
