from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins

from api.models import User, UserRole


from .serializers import UserRoleSerializer


class UserRoleReadViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,):
    serializer_class = UserRoleSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        new_queryset = UserRole.objects.filter(user=user_id)
        return new_queryset

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        user_role = serializer.validated_data.get('role')
        current_user = get_object_or_404(User, id=user_id)
        if user_role == UserRole.Role.MAIN_ADMIN:
            current_user.is_superuser = True
            current_user.is_staff = True
            current_user.save()
        serializer.save(user=current_user)

    def perform_destroy(self, instance):
        current_user = instance.user
        super().perform_destroy(instance)
        if not UserRole.objects.filter(user=current_user, role=UserRole.Role.MAIN_ADMIN).exists():
            current_user.is_superuser = False
            current_user.is_staff = False
            current_user.save()
