from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='users')

auth_urls = [
    path(
        'signup/',
        views.create_user,
        name='create_user'
    ),
    path(
        'token/',
        views.get_token,
        name='get_token'
    ),
]

v1_urls = [
    path('auth/', include(auth_urls)),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urls))
]