from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    recipe_id = serializers.IntegerField()