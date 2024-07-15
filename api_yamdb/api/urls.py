from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views
from reviews.views import CommentViewSet, ReviewViewSet

app_name = 'api'

# Создаем роутер для автоматического создания URL-ов для ViewSet-ов
router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='users')
router_v1.register('categories', views.CategoryViewSet, basename='category')
router_v1.register('genres', views.GenreViewSet, basename='genre')
router_v1.register('titles', views.TitleViewSet, basename='title')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

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
