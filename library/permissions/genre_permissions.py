from rest_framework.permissions import BasePermission


class CanGetStatisticPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('library.can_get_statistic')
