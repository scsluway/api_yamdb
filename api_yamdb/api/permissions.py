from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUser(BasePermission):
    """
    Разрешение, позволяющее доступ только администраторам.
    Используйте это разрешение для действий, доступных только администраторам,
    например, для управления пользователями или глобальных настроек.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class AdminOrReadOnly(BasePermission):
    """
    Разрешение, предоставляющее полный доступ администраторам и
    доступ только для чтения всем остальным.
    Используйте для ресурсов, которые могут быть изменены только
    администраторами, но доступны для просмотра всем пользователям (например,
    категории или жанры).
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class AuthorOrModerOrReadOnly(BasePermission):
    """
    Разрешение, позволяющее авторам, модераторам и администраторам
    редактировать объекты, а всем остальным - только читать.
    Используйте для ресурсов, которые создаются пользователями, но могут
    модерироваться (например, отзывы или комментарии).
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author
            )
        )


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Разрешение, предоставляющее доступ на запись только аутентифицированным
    пользователям, но разрешающее чтение всем.
    Используйте для ресурсов, которые могут создаваться любым
    аутентифицированным пользователем, но доступны для просмотра всем
    (например, произведения).
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated


class IsModeratorOrReadOnly(BasePermission):
    """
    Разрешение, предоставляющее полный доступ модераторам и
    доступ только для чтения всем остальным.
    Используйте для ресурсов, которые должны быть доступны для редактирования
    только модераторам, но могут быть просмотрены всеми пользователями.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_moderator
        )
