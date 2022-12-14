from rest_framework import permissions


class RegisterUserProfileOrAutorised(permissions.BasePermission):
    """Permission for user viewset.
    Allow POST to /users/ and GET to /users/{id} for unautorised.
    Disable GET to /users/me/ for unautorised.
    Allow GET and POST for autorised. Disable self create user for autorised.
    Allow POST abd DELETE to /subscribe/ for autorised.
    """

    def has_permission(self, request, view):
        path_end = request.path_info.split("/")[-2]
        auth_allow_methods = ("GET", "POST")
        return (
            (
                (
                    request.method in auth_allow_methods
                    or (
                        view.action == "subscribe"
                        and request.method == "DELETE"
                    )
                )
                and request.user.is_authenticated
                and view.action != "create"
            )
            or (view.action == "create" and not request.user.is_authenticated)
            or (view.action == "retrieve" and path_end != "me")
        )


class OnlyGet(permissions.BasePermission):
    """Allow only GET method."""

    def has_permission(self, request, view):
        return request.method == "GET"


class OnlyGetAutorised(permissions.BasePermission):
    """Allow GET for autorised."""

    def has_permission(self, request, view):

        return request.method == "GET" and request.user.is_authenticated


class GetOrGPPDAutorized(permissions.BasePermission):
    """Allow GET for all, but disable download_shopping_cart for non auth.
    Allow POST, PATCH and DELETE for autorized."""

    def has_permission(self, request, view):

        auth_allow_methods = ("GET", "POST", "PATCH", "DELETE")

        return (
            request.method == "GET" and view.action != "download_shopping_cart"
        ) or (
            request.user.is_authenticated
            and request.method in auth_allow_methods
        )
