from rest_framework.serializers import ModelSerializer
from api.models.user_models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "name"]
        extra_kwargs = {
            "password": {"write_only": True},  # Ensure password is write-only
        }

    def save(self, **kwargs):
        validated_data = self.validated_data  # Use validated data
        email = validated_data.get("email")
        password = validated_data.get("password")
        name = validated_data.get("name")

        # Create user instance and hash the password
        instance = self.Meta.model(
            email=email,
            username=email,  # Set the username to email
            first_name=name,
        )
        instance.set_password(password)
        instance.save()
        return instance
