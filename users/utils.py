from rest_framework import permissions
from .models import UserProfile
import logging
logger = logging.getLogger("user-utils")


class IsAuthenticatedExtendedAdmin(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        user = request.user
        if bool(user and user.is_authenticated):

            user_profile = UserProfile.objects.filter(user_id=user.id).exclude(organization__isnull=True)
            if not user_profile.exists():
                logger.error(f'User profile/organization does not exist for this user {user.username}')
                return False
            return user.groups.filter(name="admin").exists()
        return False


class IsAuthenticatedExtendedDoctor(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        user = request.user
        if bool(user and user.is_authenticated):
            user_profile = UserProfile.objects.filter(user_id=user.id).exclude(organization__isnull=True)
            if not user_profile.exists():
                logger.error(f'User profile/organization does not exist for this user {user.username}')
                return False
            return user.groups.filter(name="doctor").exists()
        return False


class IsAuthenticatedExtendedStaff(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        user = request.user
        if bool(user and user.is_authenticated):
            user_profile = UserProfile.objects.filter(user_id=user.id).exclude(organization__isnull=True)
            if not user_profile.exists():
                logger.error(f'User profile/organization does not exist for this user {user.username}')
                return False
            return user.groups.filter(name="staff").exists()
        return False
