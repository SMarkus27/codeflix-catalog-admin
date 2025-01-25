from rest_framework import serializers

class GenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())

class ListGenreResponseSerializer(serializers.Serializer):
    data = GenreOutputSerializer(many=True)

class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, data):
        return list(super().to_representation(data))


class CreateGenreInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(child=serializers.UUIDField(), required=False)


class CreateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class DeleteGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()