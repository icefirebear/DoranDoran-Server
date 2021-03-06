import jwt
import json

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import make_password

from .models import User
from .utils import *


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uid", "email", "password", "name", "role")
        extra_kwargs = {"role": {"required": False}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super(LoginUserSerializer, self).__init__(*args, **kwargs)

        username_field = get_username_field()

        self.fields[username_field] = serializers.CharField()
        self.fields["password"] = serializers.CharField(write_only=True)

    def validate(self, attrs):
        credentials = {
            "username": attrs.get(User.USERNAME_FIELD),
            "password": attrs.get("password"),
        }
        user = authenticate(**credentials)  # backend.authenticate 쓰고

        ## 여기부터 다시 하면 된다.
        if user is None:
            msg = _("User instance not exists")
            raise serializers.ValidationError(msg)

        payload = jwt_payload_handler(user)  # token에 쓸 payload 생성

        token = jwt_encode_handler(payload)  # token 생성

        return token  # token 반환


class RefreshJSONWebTokenSerializer(serializers.Serializer):
    Authorization = serializers.CharField()

    def validate(self, attrs):
        token = attrs["Authorization"].split()[1]
        payload = jwt_decode_handler(token)  # check_payload 만들어서 expired 예외처리 해줘야됨
        user = User.objects.get_by_natural_key(payload["uid"])

        orig_iat = payload["iat"]  # refresh 요청 당시 시간

        if orig_iat:
            refresh_limit = settings.JWT_AUTH["JWT_REFRESH_EXPIRATION_DELTA"]

            if isinstance(refresh_limit, timedelta):
                refresh_limit = refresh_limit.days * 24 * 3600 + refresh_limit.seconds

            expiration_time = orig_iat + int(refresh_limit)
            now_time = timegm(datetime.utcnow().utctimetuple())

            if now_time > expiration_time:
                msg = _("Refrash has expired")
                raise serializers.ValidationError(msg)
        else:
            msg = _("iat field is required")
            raise serializers.ValidationError(msg)

        new_payload = jwt_payload_handler(user)
        new_payload["iat"] = orig_iat
        return jwt_encode_handler(new_payload)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)