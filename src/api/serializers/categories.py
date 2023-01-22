from rest_framework import serializers

from src.teasers.models import Category


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'created', 'modified')
        read_only_fields = ('created', 'modified')

    def validate_title(self, value) -> str:
        if self.Meta.model.objects.filter(title=value).exists():
            raise serializers.ValidationError('Категория должна быть уникальной')
        return value
