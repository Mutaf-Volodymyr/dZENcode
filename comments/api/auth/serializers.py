from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "re_password",
        ]

    def create(self, validated_data):
        validated_data.pop("re_password")
        password = validated_data.get("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        password = attrs.get("password")
        re_password = attrs.get("re_password")

        if self.instance is None:
            if not password:
                raise serializers.ValidationError(
                    {"password": "The field is mandatory when creating a user."}
                )
            if not re_password:
                raise serializers.ValidationError(
                    {"re_password": "The field is mandatory when creating a user."}
                )

        if password or re_password:
            if password != re_password:
                raise serializers.ValidationError(
                    {"password": "The passwords do not match."}
                )
            try:
                validate_password(password)
            except serializers.ValidationError as err:
                raise serializers.ValidationError({"password": err.messages})

        return attrs

    def validate_username(self, value):
        if len(value) < 2 or not value.isalpha():
            raise serializers.ValidationError({"username": "Invalid username."})
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": "This username is already busy."}
            )
        return value


class PasswordUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = self.context["request"].user
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate(self, attrs):
        password = attrs.get("password")
        re_password = attrs.get("re_password")

        if password and re_password:
            if password != re_password:
                raise serializers.ValidationError(
                    {"password": "Passwords do not match."}
                )
            try:
                validate_password(password)
            except serializers.ValidationError as err:
                raise serializers.ValidationError({"password": err.messages})
        else:
            raise serializers.ValidationError(
                {"password": "Both password and re_password fields are required."}
            )

        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]
