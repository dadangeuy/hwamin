from rest_framework.exceptions import MethodNotAllowed
from rest_framework.serializers import Serializer, ModelSerializer


class ReadOnlySerializer(Serializer):
    def create(self, validated_data):
        raise MethodNotAllowed

    def update(self, instance, validated_data):
        raise MethodNotAllowed


class ReadOnlyModelSerializer(ModelSerializer):
    def create(self, validated_data):
        raise MethodNotAllowed

    def update(self, instance, validated_data):
        raise MethodNotAllowed
