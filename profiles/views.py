from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProfileHomeView(APIView):
    """
    Retorna apenas um teste de funcionamento do módulo de perfis.
    Depois substituímos por StudentProfile / TeacherProfile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "message": "Profiles API funcionando!",
                "user": request.user.email,
                "role": request.user.role,
            }
        )
