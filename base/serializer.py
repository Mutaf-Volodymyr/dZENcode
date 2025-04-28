from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):

    def _get_user_by_context(self):
        return self.context["request"].user

