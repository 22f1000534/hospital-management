from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.serializers.user import UserSerializer


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = UserSerializer(self.user).data

        return data