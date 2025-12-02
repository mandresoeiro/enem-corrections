from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class MeView(APIView):
    """Retorna dados do usuário logado.

    Endpoint GET /api/accounts/me/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": user.role,
            }
        )
