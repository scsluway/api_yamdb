from api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

# Создаем роутер для автоматического создания URL-ов для ViewSet-ов
router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='users')

# URL-ы для аутентификации
auth_urls = [
    path('signup/', views.create_user, name='signup'),
    path('token/', views.get_token, name='token'),
]

# Группируем все URL-ы API v1
v1_urls = [
    path('auth/', include(auth_urls)),
    path('', include(router_v1.urls)),
]

# Основной список URL-ов
urlpatterns = [path('v1/', include(v1_urls))]
