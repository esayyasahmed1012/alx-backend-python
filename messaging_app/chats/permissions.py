from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender or request.user == obj.recipient

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.owner == request.user