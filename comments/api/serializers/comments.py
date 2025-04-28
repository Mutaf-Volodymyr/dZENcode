from rest_framework import serializers
from base.serializer import BaseSerializer
from .users import UserSerializer
from ...models import Comment


class CommentCreateDeleteSerializer(BaseSerializer):
    class Meta:
        model = Comment
        fields = [
            'text',
            'parent',
            'file',
        ]

    def validate(self, data):
        user = self._get_user_by_context()
        data["user"] = user
        return data


class CommentListSerializer(BaseSerializer):
    user = UserSerializer()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'created_at',
            'updated_at',
            'user',
            'text',
            'rating',
            'file',
            'children',
        ]

    def get_children(self, obj):
        children_comments = obj.get_children()
        return CommentListSerializer(children_comments, many=True).data


class CommentDetailUpdateSerializer(BaseSerializer):
    children = serializers.SerializerMethodField(read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'updated_at',
            'created_at',
            'user',
            'text',
            'rating',
            'file',
            'parent',
            'children',
        ]
        read_only_fields = [
            'created_at',
            'updated_at',
            'parent',
            'rating',
        ]

    def get_children(self, obj):
        children_comments = obj.get_children()
        return children_comments.values_list('id', flat=True)
