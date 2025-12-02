from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from .models import CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    """Serializer customizado para registrar usuários com campo role.

    Extende o RegisterSerializer padrão do dj-rest-auth,
    adicionando o campo `role` e salvando isso no usuário.
    """

    role = serializers.ChoiceField(
        choices=CustomUser.Role.choices,
        default=CustomUser.Role.STUDENT,
        help_text="Papel do usuário (student/teacher/admin).",
    )

    def get_cleaned_data(self):
        """Inclui o campo role nos dados limpos usados na criação do usuário."""
        cleaned_data = super().get_cleaned_data()
        cleaned_data["role"] = self.validated_data.get("role", CustomUser.Role.STUDENT)
        return cleaned_data

    def save(self, request):
        """Cria o usuário com o campo role preenchido."""
        user = super().save(request)
        user.role = self.cleaned_data.get("role", CustomUser.Role.STUDENT)
        user.save()
        return user
