from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import RegistrationSerializer, UserSerializer


class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )
