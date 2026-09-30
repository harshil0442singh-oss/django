from rest_framework.permissions import BasePermission


class IsRecruiter(BasePermission):
    message = {"message": "You need recruiter privileges to perform this action"}

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsSeeker(BasePermission):
    message = {"message": "You need seeker privileges to perform this action"}

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_staff)
